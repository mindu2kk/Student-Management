from datetime import date
from typing import Optional
from sqlalchemy import UniqueConstraint, CheckConstraint, Index
from .extensions import db


class Khoa(db.Model):
    __tablename__ = "Khoa"

    MaKhoa = db.Column(db.String(20), primary_key=True)
    TenKhoa = db.Column(db.String(255), nullable=False, unique=True)

    giang_viens = db.relationship("GiangVien", back_populates="khoa", cascade="all, delete-orphan")
    mon_hocs = db.relationship("MonHoc", back_populates="khoa", cascade="all, delete-orphan")
    lops = db.relationship("Lop", back_populates="khoa", cascade="all, delete-orphan")


class Lop(db.Model):
    __tablename__ = "Lop"

    MaLop = db.Column(db.String(20), primary_key=True)
    PhongHocChinh = db.Column(db.String(100))
    Khoa = db.Column(db.String(20), db.ForeignKey("Khoa.MaKhoa"), nullable=False)
    SiSo = db.Column(db.Integer)

    khoa = db.relationship("Khoa", back_populates="lops")
    sinh_viens = db.relationship("SinhVien", back_populates="lop")

    __table_args__ = (
        CheckConstraint('SiSo IS NULL OR SiSo >= 0', name='ck_lop_siso_nonneg'),
        Index('ix_lop_khoa', 'Khoa'),
    )


class SinhVien(db.Model):
    __tablename__ = "SinhVien"

    MaSinhVien = db.Column(db.String(20), primary_key=True)
    HoTen = db.Column(db.String(255), nullable=False)
    NgaySinh = db.Column(db.Date)
    GioiTinh = db.Column(db.String(10))
    DiaChi = db.Column(db.String(255))
    Email = db.Column(db.String(255), unique=True)
    SDT = db.Column(db.String(20))
    CCCD = db.Column(db.String(20), unique=True)
    Lop = db.Column(db.String(20), db.ForeignKey("Lop.MaLop"))

    lop = db.relationship("Lop", back_populates="sinh_viens")
    dang_kys = db.relationship("DangKy", back_populates="sinh_vien", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_sv_lop', 'Lop'),
        Index('ix_sv_email', 'Email'),
    )


class GiangVien(db.Model):
    __tablename__ = "GiangVien"

    MaGiangVien = db.Column(db.String(20), primary_key=True)
    HoVaTen = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), unique=True)
    SoDienThoai = db.Column(db.String(20))
    MaKhoa = db.Column(db.String(20), db.ForeignKey("Khoa.MaKhoa"), nullable=False)
    NgaySinh = db.Column(db.Date)
    GioiTinh = db.Column(db.String(10))
    HocVi = db.Column(db.String(50))
    HocHam = db.Column(db.String(50))

    khoa = db.relationship("Khoa", back_populates="giang_viens")
    lop_hoc_phans = db.relationship("LopHocPhan", back_populates="giang_vien")

    __table_args__ = (
        Index('ix_gv_khoa', 'MaKhoa'),
    )

class MonHoc(db.Model):
    __tablename__ = "MonHoc"

    MaMonHoc = db.Column(db.String(20), primary_key=True)
    MaKhoa = db.Column(db.String(20), db.ForeignKey("Khoa.MaKhoa"), nullable=False)
    TenMonHoc = db.Column(db.String(255), nullable=False)
    SoTinChi = db.Column(db.Integer, nullable=False)

    khoa = db.relationship("Khoa", back_populates="mon_hocs")
    lop_hoc_phans = db.relationship("LopHocPhan", back_populates="mon_hoc")

    __table_args__ = (
        CheckConstraint('SoTinChi > 0', name='ck_monhoc_sotinchi_pos'),
        UniqueConstraint('TenMonHoc', 'MaKhoa', name='uq_monhoc_ten_khoa'),
        Index('ix_mh_khoa', 'MaKhoa'),
    )


class HocKy(db.Model):
    __tablename__ = "HocKy"

    IdHocKy = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NamHoc = db.Column(db.String(20), nullable=False) 
    Ky = db.Column(db.Integer, nullable=False)        
    TuNgay = db.Column(db.Date)
    DenNgay = db.Column(db.Date)

    __table_args__ = (
        UniqueConstraint('NamHoc', 'Ky', name='uq_hocky_namhoc_ky'),
        CheckConstraint('Ky in (1,2)', name='ck_hocky_ky_valid'),
    )


class LopHocPhan(db.Model):
    __tablename__ = "LopHocPhan"

    MaLHP = db.Column(db.String(20), primary_key=True)
    MaMonHoc = db.Column(db.String(20), db.ForeignKey("MonHoc.MaMonHoc"), nullable=False)
    MaGiangVien = db.Column(db.String(20), db.ForeignKey("GiangVien.MaGiangVien"), nullable=False)
    IdHocKy = db.Column(db.Integer, db.ForeignKey("HocKy.IdHocKy"), nullable=False)
    Nhom = db.Column(db.String(10), nullable=True)      
    SucChua = db.Column(db.Integer, nullable=True)
    TrangThai = db.Column(db.String(20), nullable=True)

    mon_hoc = db.relationship("MonHoc", back_populates="lop_hoc_phans")
    giang_vien = db.relationship("GiangVien", back_populates="lop_hoc_phans")
    hoc_ky = db.relationship("HocKy")
    dang_kys = db.relationship("DangKy", back_populates="lop_hoc_phan")

    __table_args__ = (
        CheckConstraint('SucChua IS NULL OR SucChua > 0', name='ck_lhp_succhua_pos'),
        UniqueConstraint('MaMonHoc', 'IdHocKy', 'Nhom', name='uq_lhp_mon_hocky_nhom'),
        Index('ix_lhp_monhoc', 'MaMonHoc'),
        Index('ix_lhp_gv', 'MaGiangVien'),
        Index('ix_lhp_hocky', 'IdHocKy'),
    )


class LHPLich(db.Model):
    __tablename__ = "LHPLich"

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaLHP = db.Column(
        db.String(20),
        db.ForeignKey("LopHocPhan.MaLHP", ondelete="CASCADE"),
        nullable=False
    )
    Thu = db.Column(db.Integer, nullable=False)         
    TietBatDau = db.Column(db.Integer, nullable=False)
    SoTiet = db.Column(db.Integer, nullable=False)
    Phong = db.Column(db.String(20))
    CoSo = db.Column(db.String(50))

    lhp = db.relationship(
        "LopHocPhan",
        backref=db.backref("lich_hocs", cascade="all, delete-orphan")
    )

    __table_args__ = (
        CheckConstraint('Thu BETWEEN 2 AND 8', name='ck_lich_thu'),
        CheckConstraint('TietBatDau > 0 AND SoTiet > 0', name='ck_lich_tiet_pos'),
        Index('ix_lich_lhp', 'MaLHP'),
    )


class DiemDanh(db.Model):

    __tablename__ = "DiemDanh"

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaDangKy = db.Column(
        db.Integer,
        db.ForeignKey("DangKy.MaDangKy", ondelete="CASCADE"),
        nullable=False
    )
    LHPLichId = db.Column(
        db.Integer,
        db.ForeignKey("LHPLich.Id", ondelete="CASCADE"),
        nullable=False
    )
    Ngay = db.Column(db.Date, nullable=False)
    TrangThai = db.Column(db.String(10), nullable=False) 
    PhutTre = db.Column(db.Integer)
    GhiChu = db.Column(db.String(255))

    dangky = db.relationship(
        "DangKy",
        backref=db.backref("diem_danhs", cascade="all, delete-orphan")
    )
    tiet = db.relationship("LHPLich")

    __table_args__ = (
        UniqueConstraint('MaDangKy', 'LHPLichId', 'Ngay', name='uq_dd_dk_tiet_ngay'),
        Index('ix_dd_dk', 'MaDangKy'),
    )



class DangKy(db.Model):
    __tablename__ = "DangKy"

    MaDangKy = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaSinhVien = db.Column(db.String(20), db.ForeignKey("SinhVien.MaSinhVien"), nullable=False)
    MaLHP = db.Column(db.String(20), db.ForeignKey("LopHocPhan.MaLHP"), nullable=False)
    NgayDangKy = db.Column(db.Date, nullable=False, default=date.today)
    TrangThai = db.Column(db.String(20), nullable=False, default="DK") 

    sinh_vien = db.relationship("SinhVien", back_populates="dang_kys")
    lop_hoc_phan = db.relationship("LopHocPhan", back_populates="dang_kys")
    bang_diems = db.relationship("BangDiem", back_populates="dang_ky", cascade="all, delete-orphan", uselist=False)

    __table_args__ = (
        UniqueConstraint('MaSinhVien', 'MaLHP', name='uq_dk_sv_lhp'),
        Index('ix_dk_sv', 'MaSinhVien'),
        Index('ix_dk_lhp', 'MaLHP'),
    )


class BangDiem(db.Model):
    __tablename__ = "BangDiem"

    IdBangDiem = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaDangKy = db.Column(db.Integer, db.ForeignKey("DangKy.MaDangKy", ondelete="CASCADE"), nullable=False, unique=True)
    DiemChuyenCan = db.Column(db.Float)
    DiemGiuaKy = db.Column(db.Float)
    DiemCuoiKy = db.Column(db.Float)
    DiemTongKet = db.Column(db.Float)

    dang_ky = db.relationship("DangKy", back_populates="bang_diems")

    __table_args__ = (
        CheckConstraint('DiemChuyenCan IS NULL OR (DiemChuyenCan BETWEEN 0 AND 10)', name='ck_bd_cc_0_10'),
        CheckConstraint('DiemGiuaKy   IS NULL OR (DiemGiuaKy   BETWEEN 0 AND 10)', name='ck_bd_gk_0_10'),
        CheckConstraint('DiemCuoiKy   IS NULL OR (DiemCuoiKy   BETWEEN 0 AND 10)', name='ck_bd_ck_0_10'),
        CheckConstraint('DiemTongKet  IS NULL OR (DiemTongKet  BETWEEN 0 AND 10)', name='ck_bd_tk_0_10'),
    )
