-- DDL for Sequence CART_TNO_SEQ
CREATE SEQUENCE CART_TNO_SEQ
    START WITH 9
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 20;

-- DDL for Sequence MEMBER_MID_SEQ
CREATE SEQUENCE MEMBER_MID_SEQ
    START WITH 5
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 20;

-- DDL for Sequence ORDER_OID_SEQ
CREATE SEQUENCE ORDER_OID_SEQ
    START WITH 9
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 20;

-- DDL for Table CART
CREATE TABLE CART (
    MID BIGINT,
    CARTTIME VARCHAR(26),
    TNO BIGINT
);

-- DDL for Table MEMBER
CREATE TABLE MEMBER (
    MID BIGINT,
    NAME VARCHAR(128),
    ACCOUNT VARCHAR(128),
    PASSWORD VARCHAR(128),
    IDENTITY VARCHAR(128)
);

CREATE TABLE ORDER_LIST (
    OID BIGINT,
    MID BIGINT,
    ORDERTIME DATE,
    PRICE BIGINT,
    TNO BIGINT,
    trainer VARCHAR,  -- 修改為 INT 類型
    CONSTRAINT fk_trainer FOREIGN KEY (trainer) REFERENCES TRAINER(TID)
);


-- DDL for Table PRODUCT
CREATE TABLE PRODUCT (
    PID VARCHAR(26),
    PNAME VARCHAR(128),
    PRICE BIGINT,
    CATEGORY VARCHAR(128),
    PDESC TEXT
);

-- DDL for Table RECORD
CREATE TABLE RECORD (
    TNO BIGINT,
    PID VARCHAR(26),
    AMOUNT BIGINT,
    SALEPRICE BIGINT,
    TOTAL BIGINT
);

CREATE TABLE TRAINER (
    TID VARCHAR(128) PRIMARY KEY,     -- 訓練師ID，設置為主鍵
    TNAME VARCHAR(100),       -- 訓練師名稱
    SPECIALTY VARCHAR(100)    -- 訓練師專業領域
);



-- Insert data into MEMBER table
INSERT INTO MEMBER (MID, NAME, ACCOUNT, PASSWORD, IDENTITY)
VALUES ('1', '王大明', 'MINGWANG', 'TEST', 'user');
INSERT INTO MEMBER (MID, NAME, ACCOUNT, PASSWORD, IDENTITY)
VALUES ('2', '孫小美', 'MAY', 'TEST', 'user');
INSERT INTO MEMBER (MID, NAME, ACCOUNT, PASSWORD, IDENTITY)
VALUES ('3', '林大偉', 'WEILIN', 'TEST', 'user');
INSERT INTO MEMBER (MID, NAME, ACCOUNT, PASSWORD, IDENTITY)
VALUES ('4', '陳美環', 'MAYCHANG', 'TEST', 'user');




-- Insert data into PRODUCT table
INSERT INTO PRODUCT (PID, PNAME, PRICE, CATEGORY, PDESC)
VALUES ('U58046', 'Cardio 1234', 888, 'Cardio', '進行心肺耐力訓練的基本概念和技巧，提升心血管健康。這些運動幫助增強心臟和肺部的功能，並提升整體體能。心肺運動不僅有助於減少體脂肪，還能提升耐力，減少心血管疾病的風險。保持健康的心臟是每個運動者的基本目標。');
INSERT INTO PRODUCT (PID, PNAME, PRICE, CATEGORY, PDESC)
VALUES ('V00111', 'Strength Training Heroes', 400, 'Strength Training', '這套訓練影片專注於強化肌肉力量，幫助你有效提升各部位的肌肉質量。運用強度訓練原則，從復合動作到單關節練習，每一個訓練動作都設計來增加肌肉負荷，從而增強力量與耐力，塑造結實的身形。這是為每一位想要在肌肉發展和力量增強上取得突破的訓練者提供的最佳工具。');
INSERT INTO PRODUCT (PID, PNAME, PRICE, CATEGORY, PDESC)
VALUES ('D11222', 'Flexibility & Balance Album', 300, 'Flexibility & Balance', '這張專輯設計了各種伸展運動，目的是提高身體的柔韌性和靈活度，並且幫助改善身體的平衡感。每個動作都能有效釋放肌肉的緊張感，促進關節靈活性，讓你在日常生活和運動中更加自如。無論是瑜伽、普拉提還是基本的伸展練習，這些運動都有助於提升整體體態和運動表現。');
INSERT INTO PRODUCT (PID, PNAME, PRICE, CATEGORY, PDESC)
VALUES ('B20666', 'Cardio Advanced', 500, 'Cardio', '深入了解高強度間歇訓練（HIIT）和長時間耐力運動的技巧，專為提高心肺功能和燃脂效果設計。此課程包括一系列有氧運動，將幫助你燃燒更多熱量，同時提升體力和耐力，是健身愛好者理想的選擇。持之以恆地進行這些運動將改善心血管健康，增強全身的氧氣運輸能力。');
INSERT INTO PRODUCT (PID, PNAME, PRICE, CATEGORY, PDESC)
VALUES ('B10234', 'Cardio Training Systems Introduction', 600, 'Cardio', '這本書介紹了心肺運動的基本概念和訓練方法，並深入探討了如何利用心率訓練來提升有氧耐力和體能。書中包括多種訓練模式，幫助你根據自己的目標進行調整，無論是減脂、提升體能還是增強心血管健康，都是十分有效的訓練方式。');
INSERT INTO PRODUCT (PID, PNAME, PRICE, CATEGORY, PDESC)
VALUES ('B40555', 'Strength Training Theory and Practice', 550, 'Strength Training', '這本書詳細介紹了強度訓練的理論基礎和實際應用，從肌肉解剖學到訓練計劃設計，再到不同的力量訓練技巧，都是訓練者必備的知識。書中的內容強調了各類力量訓練動作的正確姿勢，並提供了針對不同目標的訓練計劃。適合想要增強肌肉力量或提高運動表現的健身愛好者。');
INSERT INTO PRODUCT (PID, PNAME, PRICE, CATEGORY, PDESC)
VALUES ('N41023', 'Flexibility & Balance Training', 400, 'Flexibility & Balance', '這個訓練程式專注於伸展和加強身體平衡，特別適合那些希望改善身體靈活性和協調性的運動者。課程包括伸展、瑜伽和平衡練習，旨在提高關節的靈活度和身體的穩定性，讓你在其他運動中表現更加出色。平衡訓練有助於預防傷害，提升身體控制能力。');




------order_list----------
-- T001 負責 3 條訂單
INSERT INTO ORDER_LIST (OID, MID, ORDERTIME, PRICE, TNO, trainer)
VALUES (1, 4, '2021-07-04', 4350, 1, 'T001');  
INSERT INTO ORDER_LIST (OID, MID, ORDERTIME, PRICE, TNO, trainer)
VALUES (2, 1, '2021-04-26', 1500, 2, 'T001');  
INSERT INTO ORDER_LIST (OID, MID, ORDERTIME, PRICE, TNO, trainer)
VALUES (6, 5, '2021-09-15', 1200, 6, 'T001');  
-- T002 負責 2 條訂單
INSERT INTO ORDER_LIST (OID, MID, ORDERTIME, PRICE, TNO, trainer)
VALUES (3, 2, '2021-08-18', 1300, 3, 'T002');  
-- T004 負責 1 條訂單
INSERT INTO ORDER_LIST (OID, MID, ORDERTIME, PRICE, TNO, trainer)
VALUES (4, 3, '2021-05-31', 800, 4, 'T004');  
-- T005 負責 3 條訂單
INSERT INTO ORDER_LIST (OID, MID, ORDERTIME, PRICE, TNO, trainer)
VALUES (5, 2, '2021-12-09', 700, 5, 'T005');  



-------reccord
-- T002 負責的記錄
INSERT INTO RECORD (TNO, PID, AMOUNT, SALEPRICE, TOTAL)
VALUES (2, 'B10234', 1, 600, 600);

-- T003 負責的記錄
INSERT INTO RECORD (TNO, PID, AMOUNT, SALEPRICE, TOTAL)
VALUES (3, 'V00111', 1, 400, 400);

-- T004 負責的記錄
INSERT INTO RECORD (TNO, PID, AMOUNT, SALEPRICE, TOTAL)
VALUES (4, 'N41023', 2, 400, 800);

-- T005 負責的記錄
INSERT INTO RECORD (TNO, PID, AMOUNT, SALEPRICE, TOTAL)
VALUES (5, 'B20777', 2, 350, 700);
INSERT INTO RECORD (TNO, PID, AMOUNT, SALEPRICE, TOTAL)
VALUES (5, 'B40555', 2, 550, 1100);
INSERT INTO RECORD (TNO, PID, AMOUNT, SALEPRICE, TOTAL)
VALUES (5, 'N41023', 1, 400, 400);  



INSERT INTO TRAINER (TID, TNAME, SPECIALTY) VALUES 
('T001', '王小明', '瑜伽'),
('T002', '李美麗', '重量訓練'),
('T003', '陳大強', '有氧運動'),
('T004', '林佳佳', '搏擊訓練'),
('T005', '張志豪', '核心訓練');




-- DDL for Trigger MEMBER_TRG
CREATE OR REPLACE FUNCTION SET_MEMBER_MID() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.MID IS NULL THEN
        NEW.MID := NEXTVAL('MEMBER_MID_SEQ');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER MEMBER_TRG
BEFORE INSERT ON MEMBER
FOR EACH ROW
EXECUTE FUNCTION SET_MEMBER_MID();

-- DDL for Trigger ORDER_TRG
CREATE OR REPLACE FUNCTION SET_ORDER_OID() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.OID IS NULL THEN
        NEW.OID := NEXTVAL('ORDER_OID_SEQ');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER ORDER_TRG
BEFORE INSERT ON ORDER_LIST
FOR EACH ROW
EXECUTE FUNCTION SET_ORDER_OID();

