print("CourseHub - Buoi 1")

students = [
    {"id": "22000001", "name": "Nguyen Minh Anh", "major": "KHDL"},
    {"id": "22000002", "name": "Tran Duc Long", "major": "KHDL"},
]
courses = [
    {
        "code": "INT2204",
        "name": "Co so du lieu Web va he thong thong tin",
        "capacity": 3,
        "enrolled": 2,
    },
    {
        "code": "INT2205",
        "name": "Khai pha du lieu",
        "capacity": 2,
        "enrolled": 2,
    },
]
enrollments = [{"student_id": "22000001", "course_code": "INT2204"}]

for course in courses:
    remaining = course["capacity"] - course["enrolled"]
    print(course["code"], "- con", remaining, "cho")

def find_course(course_code):
    for course in courses:
        if course["code"] == course_code:
            return course
    return None

print (find_course("INT2204"))

def can_enroll(student_id, course_code):
    course = find_course(course_code)
    if course is None:
        return False, "Hoc phan khong ton tai"
    
    if course["enrolled"] >= course["capacity"]:
        return False, "Lop da du so luong"
    
    duplicated = any(
        item["student_id"] == student_id and item["course_code"] == course_code
        for item in enrollments
    )
    if duplicated:
        return False, "Sinh vien da dang ky hoc phan nay"
    
    return True, "Co the dang ky"

print(can_enroll("22000002", "INT2204"))

try:
    limit = int(input("Nhap so luong hoc phan muon hien thi: "))
    print(courses[:limit])
except ValueError:
    print("So luong phai la so nguyen")

def search_courses(keyword):
    normalized = keyword.strip().lower()
    results = []
    for course in courses:
        code = course["code"].lower()
        name = course["name"].lower()
        if normalized in code or normalized in name:
            results.append(course)
    return results

print(search_courses("web"))

def find_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None

def find_course(course_code):
    for course in courses:
        if course["code"] == course_code:
            return course
    return None

def enroll_student(student_id, course_code):
    if not find_student(student_id):
        return False, f"Sinh vien '{student_id}' khong ton tai."

    course = find_course(course_code)
    if not course:
        return False, f"Hoc phan '{course_code}' khong ton tai."

    is_duplicated = any(
        item["student_id"] == student_id and item["course_code"] == course_code
        for item in enrollments
    )

    if is_duplicated:
        return False, f"Sinh vien '{student_id}' da dang ky hoc phan '{course_code}'."

    if course["enrolled"] >= course["capacity"]:
        return False, f"Hoc phan '{course_code}' da het cho"

    enrollments.append({"student_id": student_id, "course_code": course_code})
    course["enrolled"] += 1

    return True, f"Sinh vien '{student_id}' da dang ky hoc phan '{course_code}' thanh cong"

print("\nTest 5 tinh huong dang ky hoc phan:")

test_cases = [
    ("22000002", "INT2204", "1. Đăng ký thành công (Còn chỗ, SV & HP tồn tại)"),
    ("22000001", "INT2204", "2. Đăng ký trùng (22000001 đã đăng ký INT2204)"),
    ("22000002", "INT2205", "3. Lớp đầy (INT2205 có capacity=2, enrolled=2)"),
    ("22000002", "INT9999", "4. Mã học phần không tồn tại"),
    ("99999999", "INT2204", "5. Mã sinh viên không tồn tại"),
]

for idx, (s_id, c_code, desc) in enumerate(test_cases, 1):
    success, message = enroll_student(s_id, c_code)
    print(f"\n[{desc}]")
    print(f"  Input : student_id='{s_id}', course_code='{c_code}'")
    print(f"  Output: {message}")

#Test case tren duoc tao boi cong cu Gemini AI de ho tro kiem tra tinh dung sai cua ham