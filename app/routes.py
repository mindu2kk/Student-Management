from datetime import date
from typing import Any, Dict

from flask import Blueprint, request, jsonify, abort

from .extensions import db
from .models import (
    Khoa,
    Lop,
    SinhVien,
    GiangVien,
    MonHoc,
    LopHocPhan,
    DangKy,
    BangDiem,
)


api_bp = Blueprint("api", __name__)


def parse_date(value: str | None):
    if not value:
        return None
    return date.fromisoformat(value)


def commit_or_400():
    try:
        db.session.commit()
    except Exception as exc:  # pragma: no cover - simplified error handling
        db.session.rollback()
        abort(400, description=str(exc))


# ---- Helper CRUD factory functions ----
def get_or_404(model, ident):
    obj = db.session.get(model, ident)
    if not obj:
        abort(404)
    return obj


# ---- Khoa ----
@api_bp.post("/khoas")
def create_khoa():
    data = request.get_json() or {}
    obj = Khoa(MaKhoa=data["MaKhoa"], TenKhoa=data["TenKhoa"])
    db.session.add(obj)
    commit_or_400()
    return jsonify({"MaKhoa": obj.MaKhoa, "TenKhoa": obj.TenKhoa}), 201


@api_bp.get("/khoas")
def list_khoa():
    items = Khoa.query.all()
    return jsonify([{"MaKhoa": i.MaKhoa, "TenKhoa": i.TenKhoa} for i in items])


@api_bp.get("/khoas/<ma_khoa>")
def get_khoa(ma_khoa: str):
    i = get_or_404(Khoa, ma_khoa)
    return jsonify({"MaKhoa": i.MaKhoa, "TenKhoa": i.TenKhoa})


@api_bp.put("/khoas/<ma_khoa>")
def update_khoa(ma_khoa: str):
    i = get_or_404(Khoa, ma_khoa)
    data = request.get_json() or {}
    if "TenKhoa" in data:
        i.TenKhoa = data["TenKhoa"]
    commit_or_400()
    return jsonify({"MaKhoa": i.MaKhoa, "TenKhoa": i.TenKhoa})


@api_bp.delete("/khoas/<ma_khoa>")
def delete_khoa(ma_khoa: str):
    i = get_or_404(Khoa, ma_khoa)
    db.session.delete(i)
    commit_or_400()
    return "", 204


# ---- Lop ----
@api_bp.post("/lops")
def create_lop():
    data = request.get_json() or {}
    obj = Lop(
        MaLop=data["MaLop"],
        PhongHocChinh=data.get("PhongHocChinh"),
        Khoa=data["Khoa"],
        SiSo=data.get("SiSo"),
    )
    db.session.add(obj)
    commit_or_400()
    return jsonify({"MaLop": obj.MaLop}), 201


@api_bp.get("/lops")
def list_lop():
    items = Lop.query.all()
    return jsonify([
        {
            "MaLop": i.MaLop,
            "PhongHocChinh": i.PhongHocChinh,
            "Khoa": i.Khoa,
            "SiSo": i.SiSo,
        }
        for i in items
    ])


@api_bp.get("/lops/<ma_lop>")
def get_lop(ma_lop: str):
    i = get_or_404(Lop, ma_lop)
    return jsonify({
        "MaLop": i.MaLop,
        "PhongHocChinh": i.PhongHocChinh,
        "Khoa": i.Khoa,
        "SiSo": i.SiSo,
    })


@api_bp.put("/lops/<ma_lop>")
def update_lop(ma_lop: str):
    i = get_or_404(Lop, ma_lop)
    data = request.get_json() or {}
    for f in ["PhongHocChinh", "Khoa", "SiSo"]:
        if f in data:
            setattr(i, f, data[f])
    commit_or_400()
    return jsonify({
        "MaLop": i.MaLop,
        "PhongHocChinh": i.PhongHocChinh,
        "Khoa": i.Khoa,
        "SiSo": i.SiSo,
    })


@api_bp.delete("/lops/<ma_lop>")
def delete_lop(ma_lop: str):
    i = get_or_404(Lop, ma_lop)
    db.session.delete(i)
    commit_or_400()
    return "", 204


# ---- SinhVien ----
@api_bp.post("/sinhviens")
def create_sinh_vien():
    data = request.get_json() or {}
    obj = SinhVien(
        MaSinhVien=data["MaSinhVien"],
        HoTen=data["HoTen"],
        NgaySinh=parse_date(data.get("NgaySinh")),
        GioiTinh=data.get("GioiTinh"),
        DiaChi=data.get("DiaChi"),
        Email=data.get("Email"),
        SDT=data.get("SDT"),
        CCCD=data.get("CCCD"),
        Lop=data.get("Lop"),
    )
    db.session.add(obj)
    commit_or_400()
    return jsonify({"MaSinhVien": obj.MaSinhVien}), 201


@api_bp.get("/sinhviens")
def list_sinh_vien():
    items = SinhVien.query.all()
    return jsonify([
        {
            "MaSinhVien": i.MaSinhVien,
            "HoTen": i.HoTen,
            "NgaySinh": i.NgaySinh.isoformat() if i.NgaySinh else None,
            "GioiTinh": i.GioiTinh,
            "DiaChi": i.DiaChi,
            "Email": i.Email,
            "SDT": i.SDT,
            "CCCD": i.CCCD,
            "Lop": i.Lop,
        }
        for i in items
    ])


@api_bp.get("/sinhviens/<ma_sinh_vien>")
def get_sinh_vien(ma_sinh_vien: str):
    i = get_or_404(SinhVien, ma_sinh_vien)
    return jsonify({
        "MaSinhVien": i.MaSinhVien,
        "HoTen": i.HoTen,
        "NgaySinh": i.NgaySinh.isoformat() if i.NgaySinh else None,
        "GioiTinh": i.GioiTinh,
        "DiaChi": i.DiaChi,
        "Email": i.Email,
        "SDT": i.SDT,
        "CCCD": i.CCCD,
        "Lop": i.Lop,
    })


@api_bp.put("/sinhviens/<ma_sinh_vien>")
def update_sinh_vien(ma_sinh_vien: str):
    i = get_or_404(SinhVien, ma_sinh_vien)
    data = request.get_json() or {}
    if "NgaySinh" in data:
        data["NgaySinh"] = parse_date(data.get("NgaySinh"))
    for f in ["HoTen", "NgaySinh", "GioiTinh", "DiaChi", "Email", "SDT", "CCCD", "Lop"]:
        if f in data:
            setattr(i, f, data[f])
    commit_or_400()
    return jsonify({"MaSinhVien": i.MaSinhVien})


@api_bp.delete("/sinhviens/<ma_sinh_vien>")
def delete_sinh_vien(ma_sinh_vien: str):
    i = get_or_404(SinhVien, ma_sinh_vien)
    db.session.delete(i)
    commit_or_400()
    return "", 204


# ---- GiangVien ----
@api_bp.post("/giangviens")
def create_giang_vien():
    data = request.get_json() or {}
    obj = GiangVien(
        MaGiangVien=data["MaGiangVien"],
        HoVaTen=data["HoVaTen"],
        Email=data.get("Email"),
        SoDienThoai=data.get("SoDienThoai"),
        MaKhoa=data["MaKhoa"],
        NgaySinh=parse_date(data.get("NgaySinh")),
        GioiTinh=data.get("GioiTinh"),
        HocVi=data.get("HocVi"),
        HocHam=data.get("HocHam"),
    )
    db.session.add(obj)
    commit_or_400()
    return jsonify({"MaGiangVien": obj.MaGiangVien}), 201


@api_bp.get("/giangviens")
def list_giang_vien():
    items = GiangVien.query.all()
    return jsonify([
        {
            "MaGiangVien": i.MaGiangVien,
            "HoVaTen": i.HoVaTen,
            "Email": i.Email,
            "SoDienThoai": i.SoDienThoai,
            "MaKhoa": i.MaKhoa,
            "NgaySinh": i.NgaySinh.isoformat() if i.NgaySinh else None,
            "GioiTinh": i.GioiTinh,
            "HocVi": i.HocVi,
            "HocHam": i.HocHam,
        }
        for i in items
    ])


@api_bp.get("/giangviens/<ma_giang_vien>")
def get_giang_vien(ma_giang_vien: str):
    i = get_or_404(GiangVien, ma_giang_vien)
    return jsonify({
        "MaGiangVien": i.MaGiangVien,
        "HoVaTen": i.HoVaTen,
        "Email": i.Email,
        "SoDienThoai": i.SoDienThoai,
        "MaKhoa": i.MaKhoa,
        "NgaySinh": i.NgaySinh.isoformat() if i.NgaySinh else None,
        "GioiTinh": i.GioiTinh,
        "HocVi": i.HocVi,
        "HocHam": i.HocHam,
    })


@api_bp.put("/giangviens/<ma_giang_vien>")
def update_giang_vien(ma_giang_vien: str):
    i = get_or_404(GiangVien, ma_giang_vien)
    data = request.get_json() or {}
    if "NgaySinh" in data:
        data["NgaySinh"] = parse_date(data.get("NgaySinh"))
    for f in ["HoVaTen", "Email", "SoDienThoai", "MaKhoa", "NgaySinh", "GioiTinh", "HocVi", "HocHam"]:
        if f in data:
            setattr(i, f, data[f])
    commit_or_400()
    return jsonify({"MaGiangVien": i.MaGiangVien})


@api_bp.delete("/giangviens/<ma_giang_vien>")
def delete_giang_vien(ma_giang_vien: str):
    i = get_or_404(GiangVien, ma_giang_vien)
    db.session.delete(i)
    commit_or_400()
    return "", 204


# ---- MonHoc ----
@api_bp.post("/monhocs")
def create_mon_hoc():
    data = request.get_json() or {}
    obj = MonHoc(
        MaMonHoc=data["MaMonHoc"],
        MaKhoa=data["MaKhoa"],
        TenMonHoc=data["TenMonHoc"],
        SoTinChi=data["SoTinChi"],
    )
    db.session.add(obj)
    commit_or_400()
    return jsonify({"MaMonHoc": obj.MaMonHoc}), 201


@api_bp.get("/monhocs")
def list_mon_hoc():
    items = MonHoc.query.all()
    return jsonify([
        {
            "MaMonHoc": i.MaMonHoc,
            "MaKhoa": i.MaKhoa,
            "TenMonHoc": i.TenMonHoc,
            "SoTinChi": i.SoTinChi,
        }
        for i in items
    ])


@api_bp.get("/monhocs/<ma_mon_hoc>")
def get_mon_hoc(ma_mon_hoc: str):
    i = get_or_404(MonHoc, ma_mon_hoc)
    return jsonify({
        "MaMonHoc": i.MaMonHoc,
        "MaKhoa": i.MaKhoa,
        "TenMonHoc": i.TenMonHoc,
        "SoTinChi": i.SoTinChi,
    })


@api_bp.put("/monhocs/<ma_mon_hoc>")
def update_mon_hoc(ma_mon_hoc: str):
    i = get_or_404(MonHoc, ma_mon_hoc)
    data = request.get_json() or {}
    for f in ["MaKhoa", "TenMonHoc", "SoTinChi"]:
        if f in data:
            setattr(i, f, data[f])
    commit_or_400()
    return jsonify({"MaMonHoc": i.MaMonHoc})


@api_bp.delete("/monhocs/<ma_mon_hoc>")
def delete_mon_hoc(ma_mon_hoc: str):
    i = get_or_404(MonHoc, ma_mon_hoc)
    db.session.delete(i)
    commit_or_400()
    return "", 204


# ---- LopHocPhan ----
@api_bp.post("/lophocphans")
def create_lop_hoc_phan():
    data = request.get_json() or {}
    obj = LopHocPhan(
        MaLop=data["MaLop"],
        MaMonHoc=data["MaMonHoc"],
        MaGiangVien=data["MaGiangVien"],
        HocKy=data["HocKy"],
        NamHoc=data["NamHoc"],
    )
    db.session.add(obj)
    commit_or_400()
    return jsonify({"MaLop": obj.MaLop}), 201


@api_bp.get("/lophocphans")
def list_lop_hoc_phan():
    items = LopHocPhan.query.all()
    return jsonify([
        {
            "MaLop": i.MaLop,
            "MaMonHoc": i.MaMonHoc,
            "MaGiangVien": i.MaGiangVien,
            "HocKy": i.HocKy,
            "NamHoc": i.NamHoc,
        }
        for i in items
    ])


@api_bp.get("/lophocphans/<ma_lop>")
def get_lop_hoc_phan(ma_lop: str):
    i = get_or_404(LopHocPhan, ma_lop)
    return jsonify({
        "MaLop": i.MaLop,
        "MaMonHoc": i.MaMonHoc,
        "MaGiangVien": i.MaGiangVien,
        "HocKy": i.HocKy,
        "NamHoc": i.NamHoc,
    })


@api_bp.put("/lophocphans/<ma_lop>")
def update_lop_hoc_phan(ma_lop: str):
    i = get_or_404(LopHocPhan, ma_lop)
    data = request.get_json() or {}
    for f in ["MaMonHoc", "MaGiangVien", "HocKy", "NamHoc"]:
        if f in data:
            setattr(i, f, data[f])
    commit_or_400()
    return jsonify({"MaLop": i.MaLop})


@api_bp.delete("/lophocphans/<ma_lop>")
def delete_lop_hoc_phan(ma_lop: str):
    i = get_or_404(LopHocPhan, ma_lop)
    db.session.delete(i)
    commit_or_400()
    return "", 204


# ---- DangKy ----
@api_bp.post("/dangky")
def create_dang_ky():
    data = request.get_json() or {}
    obj = DangKy(
        MaSinhVien=data["MaSinhVien"],
        MaLop=data["MaLop"],
        NgayDangKy=parse_date(data.get("NgayDangKy")) or date.today(),
    )
    db.session.add(obj)
    commit_or_400()
    return jsonify({"MaDangKy": obj.MaDangKy}), 201


@api_bp.get("/dangky/by-student/<ma_sinh_vien>")
def list_dang_ky_by_student(ma_sinh_vien: str):
    items = DangKy.query.filter_by(MaSinhVien=ma_sinh_vien).all()
    return jsonify([
        {
            "MaDangKy": i.MaDangKy,
            "MaSinhVien": i.MaSinhVien,
            "MaLop": i.MaLop,
            "NgayDangKy": i.NgayDangKy.isoformat(),
        }
        for i in items
    ])


@api_bp.get("/dangky/<int:ma_dang_ky>")
def get_dang_ky(ma_dang_ky: int):
    i = get_or_404(DangKy, ma_dang_ky)
    return jsonify({
        "MaDangKy": i.MaDangKy,
        "MaSinhVien": i.MaSinhVien,
        "MaLop": i.MaLop,
        "NgayDangKy": i.NgayDangKy.isoformat(),
    })


@api_bp.put("/dangky/<int:ma_dang_ky>")
def update_dang_ky(ma_dang_ky: int):
    i = get_or_404(DangKy, ma_dang_ky)
    data = request.get_json() or {}
    if "NgayDangKy" in data:
        data["NgayDangKy"] = parse_date(data.get("NgayDangKy"))
    for f in ["MaSinhVien", "MaLop", "NgayDangKy"]:
        if f in data:
            setattr(i, f, data[f])
    commit_or_400()
    return jsonify({"MaDangKy": i.MaDangKy})


@api_bp.delete("/dangky/<int:ma_dang_ky>")
def delete_dang_ky(ma_dang_ky: int):
    i = get_or_404(DangKy, ma_dang_ky)
    db.session.delete(i)
    commit_or_400()
    return "", 204


# ---- BangDiem ----
@api_bp.post("/bangdiem")
def create_or_update_bang_diem():
    data = request.get_json() or {}
    ma_dk = data["MaDangKy"]
    record = BangDiem.query.filter_by(MaDangKy=ma_dk).one_or_none()
    if record is None:
        record = BangDiem(MaDangKy=ma_dk)
        db.session.add(record)

    for field in [
        "DiemChuyenCan",
        "DiemGiuaKy",
        "DiemCuoiKy",
        "DiemTongKet",
    ]:
        if field in data:
            setattr(record, field, data[field])

    commit_or_400()
    return jsonify({"IdBangDiem": record.IdBangDiem, "MaDangKy": record.MaDangKy})


@api_bp.get("/bangdiem/by-registration/<int:ma_dang_ky>")
def get_bang_diem(ma_dang_ky: int):
    record = BangDiem.query.filter_by(MaDangKy=ma_dang_ky).one_or_none()
    if not record:
        abort(404)
    return jsonify(
        {
            "IdBangDiem": record.IdBangDiem,
            "MaDangKy": record.MaDangKy,
            "DiemChuyenCan": record.DiemChuyenCan,
            "DiemGiuaKy": record.DiemGiuaKy,
            "DiemCuoiKy": record.DiemCuoiKy,
            "DiemTongKet": record.DiemTongKet,
        }
    )


@api_bp.get("/bangdiem/<int:id_bang_diem>")
def get_bang_diem_by_id(id_bang_diem: int):
    record = get_or_404(BangDiem, id_bang_diem)
    return jsonify(
        {
            "IdBangDiem": record.IdBangDiem,
            "MaDangKy": record.MaDangKy,
            "DiemChuyenCan": record.DiemChuyenCan,
            "DiemGiuaKy": record.DiemGiuaKy,
            "DiemCuoiKy": record.DiemCuoiKy,
            "DiemTongKet": record.DiemTongKet,
        }
    )


@api_bp.put("/bangdiem/<int:id_bang_diem>")
def update_bang_diem(id_bang_diem: int):
    record = get_or_404(BangDiem, id_bang_diem)
    data = request.get_json() or {}
    for field in ["DiemChuyenCan", "DiemGiuaKy", "DiemCuoiKy", "DiemTongKet"]:
        if field in data:
            setattr(record, field, data[field])
    commit_or_400()
    return jsonify({"IdBangDiem": record.IdBangDiem})


@api_bp.delete("/bangdiem/<int:id_bang_diem>")
def delete_bang_diem(id_bang_diem: int):
    record = get_or_404(BangDiem, id_bang_diem)
    db.session.delete(record)
    commit_or_400()
    return "", 204


