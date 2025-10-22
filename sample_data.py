# -*- coding: utf-8 -*-
"""
sample_data.py — Seed 20 rows per table for the Student Management schema using SQLAlchemy ORM.

How to run (try in order):
1) With app factory (recommended):
   $ export FLASK_APP=app:create_app   # if your factory is app.create_app
   $ python sample_data.py

2) If your project doesn't use a factory but exposes `app` directly in app/__init__.py:
   $ python sample_data.py

3) If your models live at top-level (models.py, extensions.py in same dir):
   $ python sample_data.py

The script tries these imports automatically:
- app.create_app / app.app, app.extensions.db, app.models
- extensions / models (top-level)

It is idempotent: running multiple times will not duplicate rows.
"""

from __future__ import annotations
import sys
from datetime import date
from typing import Optional

_db = _app = None
_models = {}

def _try_imports():
    global _db, _app, _models

    try:
        from app import create_app as _create_app 
        from app.extensions import db as _db_mod 
        from app.models import (
            Khoa, Lop, SinhVien, GiangVien, MonHoc, HocKy,
            LopHocPhan, LHPLich, DangKy, BangDiem
        ) 

        app = _create_app()  # create Flask app
        _db = _db_mod
        _models.update(locals())
        return app
    except Exception as e:
        pass

    try:
        from app import app as _existing_app
        from app.extensions import db as _db_mod 
        from app.models import (
            Khoa, Lop, SinhVien, GiangVien, MonHoc, HocKy,
            LopHocPhan, LHPLich, DangKy, BangDiem
        ) 
        _db = _db_mod
        _models.update(locals())
        return _existing_app
    except Exception:
        pass

    try:
        from extensions import db as _db_mod  # type: ignore
        from models import (
            Khoa, Lop, SinhVien, GiangVien, MonHoc, HocKy,
            LopHocPhan, LHPLich, DangKy, BangDiem
        )  # type: ignore
        from flask import current_app
        from flask import Flask
        app = Flask(__name__)
        app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///sample.sqlite3")
        app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
        _db_mod.init_app(app)
        _db = _db_mod
        _models.update(locals())
        return app
    except Exception as e:
        print("❌ Could not import your app/extensions/models. Please adjust imports at the top of this script.")
        raise

def seed_data(db):
    Khoa = _models.get("Khoa")
    Lop = _models.get("Lop")
    SinhVien = _models.get("SinhVien")
    GiangVien = _models.get("GiangVien")
    MonHoc = _models.get("MonHoc")
    HocKy = _models.get("HocKy")
    LopHocPhan = _models.get("LopHocPhan")
    LHPLich = _models.get("LHPLich")
    DangKy = _models.get("DangKy")
    BangDiem = _models.get("BangDiem")

    # ---------- Helpers ----------
    def get_or_create(model, defaults=None, **kwargs):
        obj = model.query.filter_by(**kwargs).first()
        if obj:
            return obj, False
        params = dict(kwargs)
        if defaults:
            params.update(defaults)
        obj = model(**params)
        db.session.add(obj)
        return obj, True

    khoa_rows = [
        ("CNTT","Công nghệ thông tin"),
        ("KT","Kế toán"),
        ("QTKD","Quản trị kinh doanh"),
        ("NNA","Ngôn ngữ Anh"),
        ("NNH","Ngôn ngữ Hàn"),
        ("NNJ","Ngôn ngữ Nhật"),
        ("CNTP","Công nghệ thực phẩm"),
        ("CNM","Cơ khí – Chế tạo máy"),
        ("DTVT","Điện tử – Viễn thông"),
        ("QLNN","Quản lý nhà nước"),
        ("TMDT","Thương mại điện tử"),
        ("MKT","Marketing"),
        ("TCNH","Tài chính – Ngân hàng"),
        ("DL","Du lịch"),
        ("GD","Giáo dục học"),
        ("TTKD","Thống kê – Kinh doanh"),
        ("LKT","Luật Kinh tế"),
        ("TMQT","Thương mại quốc tế"),
        ("CNPM","Công nghệ phần mềm"),
        ("HTTT","Hệ thống thông tin"),
    ]
    for MaKhoa, TenKhoa in khoa_rows:
        get_or_create(Khoa, MaKhoa=MaKhoa, TenKhoa=TenKhoa)
    db.session.commit()

    # ---------- Lop ----------
    lop_rows = [
        ("CNTT01","A101","CNTT",45),
        ("CNTT02","A102","CNTT",48),
        ("KT01","B201","KT",40),
        ("QTKD01","C301","QTKD",42),
        ("NNA01","D101","NNA",36),
        ("NNJ01","D201","NNJ",35),
        ("CNTP01","E301","CNTP",39),
        ("DTVT01","F101","DTVT",41),
        ("CNM01","F202","CNM",38),
        ("TMDT01","A203","TMDT",47),
        ("MKT01","A204","MKT",44),
        ("DL01","C101","DL",33),
        ("TCNH01","C102","TCNH",50),
        ("GD01","G101","GD",37),
        ("HTTT01","A205","HTTT",43),
        ("LKT01","B301","LKT",40),
        ("TMQT01","C201","TMQT",45),
        ("CNPM01","A206","CNPM",46),
        ("QLNN01","B401","QLNN",42),
        ("CNM02","F203","CNM",39),
    ]
    for MaLop, PhongHocChinh, Khoa_fk, SiSo in lop_rows:
        get_or_create(Lop, MaLop=MaLop, defaults=dict(
            PhongHocChinh=PhongHocChinh, Khoa=Khoa_fk, SiSo=SiSo
        ))
    db.session.commit()

    # ---------- SinhVien ----------
    sv_rows = [
        ("SV001","Nguyễn Văn A","2003-02-15","Nam","Hà Nội","a01@sv.edu.vn","0912345001","012345678901","CNTT01"),
        ("SV002","Trần Thị B","2003-05-22","Nữ","Đà Nẵng","b02@sv.edu.vn","0912345002","012345678902","CNTT01"),
        ("SV003","Lê Văn C","2002-12-10","Nam","Hà Tĩnh","c03@sv.edu.vn","0912345003","012345678903","CNTT02"),
        ("SV004","Phạm Hồng D","2003-09-01","Nam","Hải Phòng","d04@sv.edu.vn","0912345004","012345678904","CNTT02"),
        ("SV005","Nguyễn Thị E","2004-01-21","Nữ","Nam Định","e05@sv.edu.vn","0912345005","012345678905","KT01"),
        ("SV006","Phan Minh F","2003-06-18","Nam","Huế","f06@sv.edu.vn","0912345006","012345678906","KT01"),
        ("SV007","Lý Thị G","2004-03-09","Nữ","Quảng Nam","g07@sv.edu.vn","0912345007","012345678907","QTKD01"),
        ("SV008","Nguyễn Văn H","2003-08-19","Nam","Hà Nội","h08@sv.edu.vn","0912345008","012345678908","QTKD01"),
        ("SV009","Trần Thị I","2004-11-28","Nữ","Thái Bình","i09@sv.edu.vn","0912345009","012345678909","NNA01"),
        ("SV010","Hoàng Văn K","2003-02-14","Nam","Bắc Ninh","k10@sv.edu.vn","0912345010","012345678910","NNA01"),
        ("SV011","Vũ Hồng L","2003-10-01","Nữ","Hải Dương","l11@sv.edu.vn","0912345011","012345678911","CNPM01"),
        ("SV012","Đặng Văn M","2002-05-03","Nam","Nghệ An","m12@sv.edu.vn","0912345012","012345678912","CNPM01"),
        ("SV013","Phan Anh N","2003-07-11","Nam","Hà Nội","n13@sv.edu.vn","0912345013","012345678913","CNPM01"),
        ("SV014","Nguyễn Huy O","2003-09-13","Nam","Hà Giang","o14@sv.edu.vn","0912345014","012345678914","HTTT01"),
        ("SV015","Bùi Lan P","2004-01-10","Nữ","Lạng Sơn","p15@sv.edu.vn","0912345015","012345678915","HTTT01"),
        ("SV016","Nguyễn Hương Q","2004-02-09","Nữ","Hải Phòng","q16@sv.edu.vn","0912345016","012345678916","HTTT01"),
        ("SV017","Đỗ Anh R","2002-08-07","Nam","Hà Nội","r17@sv.edu.vn","0912345017","012345678917","CNM01"),
        ("SV018","Nguyễn Đức S","2003-10-20","Nam","Quảng Ninh","s18@sv.edu.vn","0912345018","012345678918","CNM01"),
        ("SV019","Lê Hương T","2004-04-14","Nữ","Hà Nội","t19@sv.edu.vn","0912345019","012345678919","CNM02"),
        ("SV020","Phạm Quốc U","2003-12-25","Nam","Hà Nội","u20@sv.edu.vn","0912345020","012345678920","CNM02"),
    ]
    for MaSinhVien, HoTen, NgaySinh, GioiTinh, DiaChi, Email, SDT, CCCD, Lop_fk in sv_rows:
        get_or_create(SinhVien, MaSinhVien=MaSinhVien, defaults=dict(
            HoTen=HoTen, NgaySinh=date.fromisoformat(NgaySinh), GioiTinh=GioiTinh,
            DiaChi=DiaChi, Email=Email, SDT=SDT, CCCD=CCCD, Lop=Lop_fk
        ))
    db.session.commit()

    # ---------- GiangVien ----------
    gv_rows = [
        ("GV001","Trần Minh An","an@uni.edu.vn","0901234001","CNTT","1980-04-12","Nam","ThS","Giảng viên"),
        ("GV002","Nguyễn Thị Bình","binh@uni.edu.vn","0901234002","CNTT","1983-02-05","Nữ","TS","PGS"),
        ("GV003","Lê Hồng Cường","cuong@uni.edu.vn","0901234003","KT","1978-07-15","Nam","ThS","GV"),
        ("GV004","Phạm Văn Dũng","dung@uni.edu.vn","0901234004","QTKD","1985-03-12","Nam","TS","PGS"),
        ("GV005","Nguyễn Ngọc Em","em@uni.edu.vn","0901234005","NNA","1990-09-08","Nữ","ThS","GV"),
        ("GV006","Lê Văn Phong","phong@uni.edu.vn","0901234006","CNPM","1981-05-03","Nam","TS","GV"),
        ("GV007","Phạm Anh Quân","quan@uni.edu.vn","0901234007","HTTT","1986-06-16","Nam","ThS","GV"),
        ("GV008","Vũ Lan Hương","huong@uni.edu.vn","0901234008","DL","1989-12-19","Nữ","ThS","GV"),
        ("GV009","Đinh Văn Toàn","toan@uni.edu.vn","0901234009","CNM","1984-10-22","Nam","TS","PGS"),
        ("GV010","Nguyễn Quang Khải","khai@uni.edu.vn","0901234010","CNTP","1987-11-01","Nam","ThS","GV"),
        ("GV011","Đặng Quốc Việt","viet@uni.edu.vn","0901234011","LKT","1979-03-18","Nam","TS","GV"),
        ("GV012","Nguyễn Thu Thảo","thao@uni.edu.vn","0901234012","MKT","1991-08-12","Nữ","ThS","GV"),
        ("GV013","Lưu Anh Tài","tai@uni.edu.vn","0901234013","TMQT","1982-10-07","Nam","TS","GV"),
        ("GV014","Đỗ Bích Hằng","hang@uni.edu.vn","0901234014","QLNN","1985-11-09","Nữ","ThS","GV"),
        ("GV015","Nguyễn Văn Thắng","thang@uni.edu.vn","0901234015","TCNH","1977-04-21","Nam","TS","PGS"),
        ("GV016","Trần Hữu Đức","duc@uni.edu.vn","0901234016","HTTT","1988-02-14","Nam","ThS","GV"),
        ("GV017","Bùi Minh Châu","chau@uni.edu.vn","0901234017","CNPM","1986-07-25","Nữ","ThS","GV"),
        ("GV018","Nguyễn Quốc Huy","huy@uni.edu.vn","1990-10-03","CNTT","0901234018","Nam","ThS"),  # will fix order below
        ("GV019","Trần Thu Giang","giang@uni.edu.vn","0901234019","NNH","1992-09-09","Nữ","ThS","GV"),
        ("GV020","Phạm Văn Long","long@uni.edu.vn","0901234020","TMDT","1984-03-03","Nam","TS","GV"),
    ]
    gv_rows[17] = ("GV018","Nguyễn Quốc Huy","huy@uni.edu.vn","0901234018","CNTT","1990-10-03","Nam","ThS","GV")

    for (MaGiangVien, HoVaTen, Email, SoDienThoai, MaKhoa_fk, NgaySinh, GioiTinh, HocVi, HocHam) in gv_rows:
        get_or_create(GiangVien, MaGiangVien=MaGiangVien, defaults=dict(
            HoVaTen=HoVaTen, Email=Email, SoDienThoai=SoDienThoai, MaKhoa=MaKhoa_fk,
            NgaySinh=date.fromisoformat(NgaySinh), GioiTinh=GioiTinh, HocVi=HocVi, HocHam=HocHam
        ))
    db.session.commit()

    # ---------- MonHoc ----------
    mh_rows = [
        ("MH001","CNTT","Lập trình Python",3),
        ("MH002","CNTT","Cấu trúc dữ liệu",3),
        ("MH003","CNTT","Hệ điều hành",3),
        ("MH004","CNTT","Cơ sở dữ liệu",3),
        ("MH005","HTTT","Phân tích hệ thống",3),
        ("MH006","CNPM","Thiết kế phần mềm",3),
        ("MH007","CNPM","Kiểm thử phần mềm",3),
        ("MH008","QTKD","Quản trị học",3),
        ("MH009","KT","Kế toán tài chính",3),
        ("MH010","TCNH","Ngân hàng thương mại",3),
        ("MH011","MKT","Marketing căn bản",2),
        ("MH012","TMQT","Thương mại điện tử",3),
        ("MH013","NNA","Ngữ pháp tiếng Anh",3),
        ("MH014","NNH","Tiếng Hàn sơ cấp",3),
        ("MH015","NNJ","Tiếng Nhật sơ cấp",3),
        ("MH016","CNM","Vẽ kỹ thuật",2),
        ("MH017","CNTP","Công nghệ chế biến",3),
        ("MH018","LKT","Luật kinh tế",3),
        ("MH019","QLNN","Chính trị học",2),
        ("MH020","DL","Quản lý du lịch",2),
    ]
    for MaMonHoc, MaKhoa_fk, TenMonHoc, SoTinChi in mh_rows:
        get_or_create(MonHoc, MaMonHoc=MaMonHoc, defaults=dict(
            MaKhoa=MaKhoa_fk, TenMonHoc=TenMonHoc, SoTinChi=SoTinChi
        ))
    db.session.commit()

    hk_rows = []
    id_counter = 1
    start_year = 2015
    for y in range(start_year, start_year+10):
        for ky in [1,2]:
            if ky == 1:
                TuNgay = f"{y}-09-01"
                DenNgay = f"{y+1}-01-15"
            else:
                TuNgay = f"{y+1}-02-01"
                DenNgay = f"{y+1}-06-15"
            hk_rows.append((id_counter, f"{y}–{y+1}", ky, TuNgay, DenNgay))
            id_counter += 1
    hk_rows = hk_rows[:20]
    for IdHocKy, NamHoc, Ky, TuNgay, DenNgay in hk_rows:
        obj = HocKy.query.get(IdHocKy)
        if not obj:
            obj = HocKy(IdHocKy=IdHocKy, NamHoc=NamHoc, Ky=Ky,
                        TuNgay=date.fromisoformat(TuNgay),
                        DenNgay=date.fromisoformat(DenNgay))
            db.session.add(obj)
        else:
            pass
    db.session.commit()

    # ---------- LopHocPhan ----------
    lhp_rows = [
        ("LHP001","MH001","GV001",19,"N1",50,"Mở"),
        ("LHP002","MH002","GV002",19,"N1",45,"Mở"),
        ("LHP003","MH003","GV018",19,"N1",50,"Mở"),
        ("LHP004","MH004","GV006",19,"N1",40,"Mở"),
        ("LHP005","MH005","GV007",19,"N1",40,"Mở"),
        ("LHP006","MH006","GV017",19,"N1",35,"Mở"),
        ("LHP007","MH007","GV017",19,"N2",40,"Mở"),
        ("LHP008","MH008","GV004",19,"N1",45,"Mở"),
        ("LHP009","MH009","GV003",19,"N1",40,"Mở"),
        ("LHP010","MH010","GV015",19,"N1",45,"Mở"),
        ("LHP011","MH011","GV012",19,"N1",50,"Mở"),
        ("LHP012","MH012","GV020",19,"N1",50,"Mở"),
        ("LHP013","MH013","GV005",19,"N1",40,"Mở"),
        ("LHP014","MH014","GV019",19,"N1",40,"Mở"),
        ("LHP015","MH015","GV019",19,"N2",35,"Mở"),
        ("LHP016","MH016","GV009",19,"N1",30,"Mở"),
        ("LHP017","MH017","GV010",19,"N1",30,"Mở"),
        ("LHP018","MH018","GV011",19,"N1",40,"Mở"),
        ("LHP019","MH019","GV014",20,"N1",50,"Mở"),
        ("LHP020","MH020","GV008",20,"N1",30,"Mở"),
    ]
    for MaLHP, MaMonHoc_fk, MaGiangVien_fk, IdHocKy_fk, Nhom, SucChua, TrangThai in lhp_rows:
        get_or_create(LopHocPhan, MaLHP=MaLHP, defaults=dict(
            MaMonHoc=MaMonHoc_fk, MaGiangVien=MaGiangVien_fk, IdHocKy=IdHocKy_fk,
            Nhom=Nhom, SucChua=SucChua, TrangThai=TrangThai
        ))
    db.session.commit()

    # ---------- LHPLich (20 rows) ----------
    lich_rows = [
        (1,"LHP001",2,1,3,"A101","CS1"),
        (2,"LHP001",4,1,3,"A101","CS1"),
        (3,"LHP002",3,4,3,"A102","CS1"),
        (4,"LHP003",2,7,3,"A103","CS1"),
        (5,"LHP004",5,1,3,"A104","CS1"),
        (6,"LHP005",3,1,3,"A105","CS1"),
        (7,"LHP006",2,4,3,"A106","CS1"),
        (8,"LHP007",5,4,3,"A107","CS1"),
        (9,"LHP008",3,7,3,"A108","CS1"),
        (10,"LHP009",4,7,3,"A109","CS1"),
        (11,"LHP010",2,10,3,"A110","CS1"),
        (12,"LHP011",4,10,3,"A111","CS1"),
        (13,"LHP012",3,1,3,"A112","CS1"),
        (14,"LHP013",2,1,3,"A113","CS1"),
        (15,"LHP014",5,1,3,"A114","CS1"),
        (16,"LHP015",3,4,3,"A115","CS1"),
        (17,"LHP016",2,7,3,"A116","CS1"),
        (18,"LHP017",3,7,3,"A117","CS1"),
        (19,"LHP018",4,1,3,"A118","CS1"),
        (20,"LHP019",2,1,3,"A119","CS1"),
    ]
    for Id, MaLHP_fk, Thu, TietBatDau, SoTiet, Phong, CoSo in lich_rows:
        obj = LHPLich.query.get(Id)
        if not obj:
            obj = LHPLich(Id=Id, MaLHP=MaLHP_fk, Thu=Thu, TietBatDau=TietBatDau,
                          SoTiet=SoTiet, Phong=Phong, CoSo=CoSo)
            db.session.add(obj)
    db.session.commit()

    # ---------- DangKy (20 rows) ----------
    dk_rows = [
        (1,"SV001","LHP001","2024-09-01","DK"),
        (2,"SV002","LHP001","2024-09-01","DK"),
        (3,"SV003","LHP002","2024-09-02","DK"),
        (4,"SV004","LHP003","2024-09-02","DK"),
        (5,"SV005","LHP004","2024-09-02","DK"),
        (6,"SV006","LHP004","2024-09-03","DK"),
        (7,"SV007","LHP005","2024-09-03","DK"),
        (8,"SV008","LHP005","2024-09-03","DK"),
        (9,"SV009","LHP006","2024-09-04","DK"),
        (10,"SV010","LHP006","2024-09-04","DK"),
        (11,"SV011","LHP007","2024-09-04","DK"),
        (12,"SV012","LHP008","2024-09-05","DK"),
        (13,"SV013","LHP009","2024-09-05","DK"),
        (14,"SV014","LHP010","2024-09-05","DK"),
        (15,"SV015","LHP011","2024-09-06","DK"),
        (16,"SV016","LHP012","2024-09-06","DK"),
        (17,"SV017","LHP013","2024-09-06","DK"),
        (18,"SV018","LHP014","2024-09-07","DK"),
        (19,"SV019","LHP015","2024-09-07","DK"),
        (20,"SV020","LHP016","2024-09-07","DK"),
    ]
    for MaDangKy, MaSinhVien_fk, MaLHP_fk, NgayDangKy, TrangThai in dk_rows:
        obj = DangKy.query.get(MaDangKy)
        if not obj:
            obj = DangKy(MaDangKy=MaDangKy, MaSinhVien=MaSinhVien_fk, MaLHP=MaLHP_fk,
                         NgayDangKy=date.fromisoformat(NgayDangKy), TrangThai=TrangThai)
            db.session.add(obj)
    db.session.commit()

    # ---------- BangDiem (20 rows) ----------
    bd_rows = [
        (1,1,9.0,8.0,8.5,8.4),
        (2,2,8.5,7.5,8.0,8.0),
        (3,3,9.0,9.0,9.0,9.0),
        (4,4,7.0,6.5,7.5,7.1),
        (5,5,10.0,9.0,9.5,9.5),
        (6,6,8.0,7.0,7.5,7.5),
        (7,7,9.0,8.5,8.0,8.5),
        (8,8,8.5,8.0,8.5,8.4),
        (9,9,7.0,7.5,8.0,7.6),
        (10,10,9.5,9.0,9.0,9.2),
        (11,11,8.0,8.0,8.0,8.0),
        (12,12,7.5,7.0,7.0,7.2),
        (13,13,8.5,8.0,8.0,8.2),
        (14,14,6.0,6.5,7.0,6.6),
        (15,15,10.0,9.5,9.5,9.7),
        (16,16,9.0,8.5,8.5,8.7),
        (17,17,8.0,8.0,8.5,8.2),
        (18,18,7.0,7.0,7.5,7.2),
        (19,19,8.5,8.5,8.5,8.5),
        (20,20,6.5,6.0,6.0,6.2),
    ]
    for IdBangDiem, MaDangKy_fk, DiemChuyenCan, DiemGiuaKy, DiemCuoiKy, DiemTongKet in bd_rows:
        obj = BangDiem.query.get(IdBangDiem)
        if not obj:
            obj = BangDiem(
                IdBangDiem=IdBangDiem, MaDangKy=MaDangKy_fk,
                DiemChuyenCan=DiemChuyenCan, DiemGiuaKy=DiemGiuaKy,
                DiemCuoiKy=DiemCuoiKy, DiemTongKet=DiemTongKet
            )
            db.session.add(obj)
    db.session.commit()

    # ---------- DiemDanh (20 rows) ----------
    dd_rows = [
        (1,1,1,"2024-09-09","P",0,""),
        (2,1,2,"2024-09-11","P",0,""),
        (3,2,1,"2024-09-09","P",0,""),
        (4,2,2,"2024-09-11","V",0,"xin phép"),
        (5,3,3,"2024-09-10","P",0,""),
        (6,4,4,"2024-09-10","M",10,"đến muộn"),
        (7,5,5,"2024-09-13","P",0,""),
        (8,6,5,"2024-09-13","P",0,""),
        (9,7,6,"2024-09-11","P",0,""),
        (10,8,6,"2024-09-11","P",0,""),
        (11,9,7,"2024-09-12","P",0,""),
        (12,10,8,"2024-09-13","P",0,""),
        (13,11,9,"2024-09-12","P",0,""),
        (14,12,10,"2024-09-13","P",0,""),
        (15,13,11,"2024-09-09","P",0,""),
        (16,14,12,"2024-09-11","P",0,""),
        (17,15,13,"2024-09-10","P",0,""),
        (18,16,14,"2024-09-12","P",0,""),
        (19,17,15,"2024-09-13","P",0,""),
        (20,18,16,"2024-09-13","P",0,""),
    ]
    for Id, MaDangKy_fk, LHPLichId_fk, Ngay, TrangThai, PhutTre, GhiChu in dd_rows:
        obj = Bang = _ = None
        obj = _models["DiemDanh"].query.get(Id)
        if not obj:
            obj = _models["DiemDanh"](
                Id=Id, MaDangKy=MaDangKy_fk, LHPLichId=LHPLichId_fk,
                Ngay=date.fromisoformat(Ngay), TrangThai=TrangThai,
                PhutTre=PhutTre, GhiChu=GhiChu
            )
            db.session.add(obj)
    db.session.commit()

def main():
    app = _try_imports()
    with app.app_context():
        global _db
        try:
            _db.create_all()
        except Exception:
            pass
        seed_data(_db)
        print("✅ Seeded 20 rows per table successfully.")

if __name__ == "__main__":
    main()
