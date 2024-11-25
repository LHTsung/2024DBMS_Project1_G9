from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app

UPLOAD_FOLDER = 'static/product'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager = Blueprint('manager', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager.productManager'))

@manager.route('/productManager', methods=['GET', 'POST'])
@login_required
def productManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        pid = request.values.get('delete')
        data = Record.delete_check(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = Product.get_product(pid)
            Product.delete_product(pid)
    
    elif 'edit' in request.values:
        pid = request.values.get('edit')
        return redirect(url_for('manager.edit', pid=pid))
    
    book_data = book()
    return render_template('productManager.html', book_data = book_data, user=current_user.name)

def book():
    book_row = Product.get_all_product()
    book_data = []
    for i in book_row:
        book = {
            '課程編號': i[0],
            '課程名稱': i[1],
            '課程售價': i[2],
            '課程類別': i[3]
        }
        book_data.append(book)
    return book_data

@manager.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            pid = en + number
            data = Product.get_product(pid)

        pname = request.values.get('pname')
        price = request.values.get('price')
        category = request.values.get('category')
        pdesc = request.values.get('description')

        # 檢查是否正確獲取到所有欄位的數據
        if pname is None or price is None or category is None or pdesc is None:
            flash('所有欄位都是必填的，請確認輸入內容。')
            return redirect(url_for('manager.productManager'))

        # 檢查欄位的長度
        if len(pname) < 1 or len(price) < 1:
            flash('課程名稱或價格不可為空。')
            return redirect(url_for('manager.productManager'))


        if (len(pname) < 1 or len(price) < 1):
            return redirect(url_for('manager.productManager'))
        
        Product.add_product(
            {   
                'pid' : pid,
                'pname' : pname,
                'price' : price,
                'category' : category,
                'pdesc':pdesc
            }
        )

        return redirect(url_for('manager.productManager'))

    return render_template('productManager.html')

@manager.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))

    if request.method == 'POST':
        Product.update_product(
            {
            'pname' : request.values.get('pname'),
            'price' : request.values.get('price'),
            'category' : request.values.get('category'), 
            'pdesc' : request.values.get('description'),
            'pid' : request.values.get('pid')
            }
        )
        
        return redirect(url_for('manager.productManager'))

    else:
        product = show_info()
        return render_template('edit.html', data=product)


def show_info():
    pid = request.args['pid']
    data = Product.get_product(pid)
    pname = data[1]
    price = data[2]
    category = data[3]
    description = data[4]

    product = {
        '課程編號': pid,
        '課程名稱': pname,
        '單價': price,
        '類別': category,
        '課程敘述': description
    }
    return product


@manager.route('/orderManager', methods=['GET', 'POST'])
@login_required
def orderManager():
    if request.method == 'POST':
        pass
    else:
        order_row = Order_List.get_order()
        order_data = []
        for i in order_row:
            order = {
                '訂單編號': i[0],
                '訂購人': i[1],
                '訂單總價': i[2],
                '訂單時間': i[3]
            }
            order_data.append(order)
            
        orderdetail_row = Order_List.get_orderdetail()
        order_detail = []

        for j in orderdetail_row:
            orderdetail = {
                '訂單編號': j[0],
                '課程名稱': j[1],
                '課程單價': j[2],
                '訂購數量': j[3]
            }
            order_detail.append(orderdetail)

    return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)


@manager.route('/orderTracker', methods=['GET', 'POST'])
@login_required
def orderTracker():
    order_data = []
    order_detail = []
    # 獲取所有訓練員
    trainers = Trainer.get_all_trainers()

    # 處理刪除訂單
    if 'delete' in request.values:
        oid = request.values.get('delete')
        data = Record.delete_check(oid)
        print(oid)
        if data is not None:
            flash('有使用者有使用到這筆資料，所以不能刪除')
        else:
            Order_List.delete_order(oid)
            flash('訂單已刪除')
        return redirect(url_for('manager.orderTracker'))
    
    # 處理承接/取消操作
    elif 'action' in request.form:
        oid = request.form.get('oid')
        action = request.form.get('action')
        if action == '承接':
            ename = request.form.get('ename')
            print(f"承接訂單編號: {oid}, 訓練員ID: {ename}")
            if not ename:
                flash('請選擇一位訓練員進行承接')
            else:
                Order_List.update_trainer(ename, oid)
                flash('訂單已成功承接')
        elif action == '取消':
            print(f"取消訂單編號: {oid}")
            Order_List.update_trainer(None, oid)
            flash('訂單承接已取消')
        return redirect(url_for('manager.orderTracker'))

    if request.method == 'POST':
        pass
    else:
        order_row = Order_List.get_order()
        for i in order_row:
            status = "已接單" if i[4] else "未接單"
            order = {
                '訂單編號': i[0],
                '訂購人': i[1],
                '訂單總價': i[2],
                '訂單時間': i[3],
                '接單訓練員': i[4] if i[4] else '',
                '訂單狀態': status
            }
            order_data.append(order)
        
        orderdetail_row = Order_List.get_orderdetail()
        for j in orderdetail_row:
            orderdetail = {
                '訂單編號': j[0],
                '課程名稱': j[1],
                '課程單價': j[2],
                '訂購數量': j[3],
                '接單訓練員': j[4]
            }
            order_detail.append(orderdetail)
    
    return render_template('orderTracker.html', orderData=order_data, orderDetail=order_detail, trainers=trainers, user=current_user.name)


@manager.route('/toggle_status', methods=['POST'])
@login_required
def toggle_status():
    # if current_user.identity != 'admin':  # 假設管理員的身份為 'admin'
    #     flash('No permission')
    #     return redirect(url_for('index'))
    
    product_id = request.form.get('product_id')
    if product_id:
        new_status = Product.toggle_status(product_id)
        if new_status:
            flash(f'課程狀態已更新為 {new_status}')
        else:
            flash('更新狀態時發生錯誤')
    else:
        flash('無效的課程編號')
    
    return redirect(url_for('manager.productManager'))

@manager.route('/trainerManager', methods=['GET', 'POST'])
@login_required
def trainerManager():
    if current_user.role == 'user':
        flash('No permission')
        return redirect(url_for('index'))

    # 處理表單提交
    if request.method == 'POST':
        action = request.form.get('action')
        tid = request.form.get('tid')  # 確保能夠獲取 tid
        tname = request.form.get('tname')
        specialty = request.form.get('specialty')

        if not tid:
            flash("訓練員ID未正確提供")
            return redirect(url_for('manager.trainerManager'))

        if action == 'add':
            # 新增邏輯
            input_data = {
                'tid': tid,
                'tname': tname,
                'specialty': specialty
            }
            Trainer.add_trainer(input_data)
            flash('訓練員已成功新增')

        elif action == 'update':
            # 更新訓練員資料
            input_data = {
                'tid': tid,
                'tname': tname,
                'specialty': specialty
            }
            Trainer.update_trainer(input_data)
            flash('訓練員資料已更新')

        elif action == 'delete':
            # 刪除邏輯
            Trainer.delete_trainer(tid)
            flash('訓練員已刪除')

        return redirect(url_for('manager.trainerManager'))

    # 搜索功能：處理 GET 請求，根據 search 關鍵字過濾訓練員
    search_query = request.args.get('search', '')
    if search_query:
        trainer_data = Trainer.get_trainers_by_search(search_query)
    else:
        trainer_data = Trainer.get_all_trainers()

    return render_template('trainerManager.html', trainer_data=trainer_data, user=current_user.name)


@manager.route('/addTrainer', methods=['GET', 'POST'])
@login_required
def addTrainer():
    if current_user.role == 'user':
        flash('No permission')
        return redirect(url_for('index'))

    if request.method == 'POST':
        tid = request.form['tid']
        tname = request.form['tname']
        specialty = request.form['specialty']

        # 新增訓練員資料
        input_data = {
            'tid': tid,
            'tname': tname,
            'specialty': specialty
        }
        Trainer.add_trainer(input_data)
        flash('訓練員已成功新增')
        return redirect(url_for('manager.trainerManager'))

    return render_template('addTrainer.html')


@manager.route('/editTrainer/<tid>', methods=['GET', 'POST'])
@login_required
def editTrainer(tid):
    if current_user.role == 'user':
        flash('No permission')
        return redirect(url_for('index'))

    # 獲取訓練員資料
    trainer = Trainer.get_trainer(tid)
    if not trainer:
        flash("訓練員不存在")
        return redirect(url_for('manager.trainerManager'))

    if request.method == 'POST':
        tname = request.form['tname']
        specialty = request.form['specialty']

        # 更新訓練員資料
        input_data = {
            'tid': tid,
            'tname': tname,
            'specialty': specialty
        }
        Trainer.update_trainer(input_data)
        flash('訓練員資料已更新')
        return redirect(url_for('manager.trainerManager'))

    return render_template('editTrainer.html', trainer=trainer)


@manager.route('/deleteTrainer/<tid>', methods=['GET', 'POST'])
@login_required
def deleteTrainer(tid):
    if current_user.role == 'user':
        flash('No permission')
        return redirect(url_for('index'))

    # 獲取訓練員資料
    trainer = Trainer.get_trainer(tid)
    if not trainer:
        flash("訓練員不存在")
        return redirect(url_for('manager.trainerManager'))

    if request.method == 'POST':
        # 刪除訓練員
        Trainer.delete_trainer(tid)
        flash('訓練員已刪除')
        return redirect(url_for('manager.trainerManager'))

    return render_template('deleteTrainer.html', trainer=trainer)
    
    
@manager.route('/dashboard', methods=['GET', 'POST'])
@login_required  # 確保用戶已登入
def dashboard():
    return render_template('dashboard.html', user=current_user)