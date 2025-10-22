from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash

from .extensions import db
from .models import Khoa, Lop, SinhVien, GiangVien, MonHoc, LopHocPhan, DangKy, BangDiem


ui_bp = Blueprint("ui", __name__, template_folder="templates")


@ui_bp.get("/")
def home():
    return render_template("home.html")


# ---- Khoa pages ----
@ui_bp.get("/khoas")
def ui_khoas():
    items = Khoa.query.order_by(Khoa.MaKhoa).all()
    return render_template("khoa/list.html", items=items)


@ui_bp.route("/khoas/new", methods=["GET", "POST"])
def ui_khoa_new():
    if request.method == "POST":
        obj = Khoa(MaKhoa=request.form["MaKhoa"], TenKhoa=request.form["TenKhoa"])
        db.session.add(obj)
        db.session.commit()
        flash("Created department", "success")
        return redirect(url_for("ui.ui_khoas"))
    return render_template("khoa/form.html", obj=None)


@ui_bp.route("/khoas/<ma_khoa>/edit", methods=["GET", "POST"])
def ui_khoa_edit(ma_khoa: str):
    obj = db.session.get(Khoa, ma_khoa)
    if request.method == "POST":
        obj.TenKhoa = request.form["TenKhoa"]
        db.session.commit()
        flash("Updated department", "success")
        return redirect(url_for("ui.ui_khoas"))
    return render_template("khoa/form.html", obj=obj)


@ui_bp.post("/khoas/<ma_khoa>/delete")
def ui_khoa_delete(ma_khoa: str):
    obj = db.session.get(Khoa, ma_khoa)
    db.session.delete(obj)
    db.session.commit()
    flash("Deleted department", "info")
    return redirect(url_for("ui.ui_khoas"))


# ---- Similar minimal CRUD pages for Lop and SinhVien ----
@ui_bp.get("/lops")
def ui_lops():
    items = Lop.query.order_by(Lop.MaLop).all()
    khoas = Khoa.query.all()
    return render_template("lop/list.html", items=items, khoas=khoas)


@ui_bp.route("/lops/new", methods=["GET", "POST"])
def ui_lop_new():
    khoas = Khoa.query.all()
    if request.method == "POST":
        obj = Lop(
            MaLop=request.form["MaLop"],
            PhongHocChinh=request.form.get("PhongHocChinh"),
            Khoa=request.form["Khoa"],
            SiSo=int(request.form.get("SiSo") or 0),
        )
        db.session.add(obj)
        db.session.commit()
        flash("Created class", "success")
        return redirect(url_for("ui.ui_lops"))
    return render_template("lop/form.html", obj=None, khoas=khoas)


@ui_bp.route("/lops/<ma_lop>/edit", methods=["GET", "POST"])
def ui_lop_edit(ma_lop: str):
    obj = db.session.get(Lop, ma_lop)
    khoas = Khoa.query.all()
    if request.method == "POST":
        obj.PhongHocChinh = request.form.get("PhongHocChinh")
        obj.Khoa = request.form["Khoa"]
        obj.SiSo = int(request.form.get("SiSo") or 0)
        db.session.commit()
        flash("Updated class", "success")
        return redirect(url_for("ui.ui_lops"))
    return render_template("lop/form.html", obj=obj, khoas=khoas)


@ui_bp.post("/lops/<ma_lop>/delete")
def ui_lop_delete(ma_lop: str):
    obj = db.session.get(Lop, ma_lop)
    db.session.delete(obj)
    db.session.commit()
    flash("Deleted class", "info")
    return redirect(url_for("ui.ui_lops"))


@ui_bp.get("/sinhviens")
def ui_sinhviens():
    items = SinhVien.query.order_by(SinhVien.MaSinhVien).all()
    lops = Lop.query.order_by(Lop.MaLop).all()
    return render_template("sinhvien/list.html", items=items, lops=lops)


@ui_bp.route("/sinhviens/new", methods=["GET", "POST"])
def ui_sinhvien_new():
    lops = Lop.query.order_by(Lop.MaLop).all()
    if request.method == "POST":
        obj = SinhVien(
            MaSinhVien=request.form["MaSinhVien"],
            HoTen=request.form["HoTen"],
            NgaySinh=date.fromisoformat(request.form["NgaySinh"]) if request.form.get("NgaySinh") else None,
            GioiTinh=request.form.get("GioiTinh"),
            DiaChi=request.form.get("DiaChi"),
            Email=request.form.get("Email"),
            SDT=request.form.get("SDT"),
            CCCD=request.form.get("CCCD"),
            Lop=request.form.get("Lop") or None,
        )
        db.session.add(obj)
        db.session.commit()
        flash("Created student", "success")
        return redirect(url_for("ui.ui_sinhviens"))
    return render_template("sinhvien/form.html", obj=None, lops=lops)


@ui_bp.route("/sinhviens/<ma_sinh_vien>/edit", methods=["GET", "POST"])
def ui_sinhvien_edit(ma_sinh_vien: str):
    obj = db.session.get(SinhVien, ma_sinh_vien)
    lops = Lop.query.order_by(Lop.MaLop).all()
    if request.method == "POST":
        obj.HoTen = request.form["HoTen"]
        obj.NgaySinh = date.fromisoformat(request.form["NgaySinh"]) if request.form.get("NgaySinh") else None
        obj.GioiTinh = request.form.get("GioiTinh")
        obj.DiaChi = request.form.get("DiaChi")
        obj.Email = request.form.get("Email")
        obj.SDT = request.form.get("SDT")
        obj.CCCD = request.form.get("CCCD")
        obj.Lop = request.form.get("Lop") or None
        db.session.commit()
        flash("Updated student", "success")
        return redirect(url_for("ui.ui_sinhviens"))
    return render_template("sinhvien/form.html", obj=obj, lops=lops)


@ui_bp.post("/sinhviens/<ma_sinh_vien>/delete")
def ui_sinhvien_delete(ma_sinh_vien: str):
    obj = db.session.get(SinhVien, ma_sinh_vien)
    db.session.delete(obj)
    db.session.commit()
    flash("Deleted student", "info")
    return redirect(url_for("ui.ui_sinhviens"))


