from database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd,hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def check_teacher_exists(username):
    response =supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0


def create_teacher(username, password, name):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
    }

    response = supabase.table("teachers").insert(data).execute()

    return len(response.data) > 0

def teacher_login(username, password):
    response = supabase.table("teachers") \
        .select("teacher_id,username,password,name") \
        .eq("username", username) \
        .execute()

    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher

    return None

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def create_student(new_name,face_embedding=None,voice_embedding=None):
    data={
        'name':new_name,
        'face_embedding':face_embedding,
        'voice_embedding':voice_embedding
    }
    response = supabase.table('students').insert(data).execute()
    if response.data:
        return response.data[0]
    return None

def get_student_by_id(student_id):
    try:
        response = (
            supabase.table("students")
            .select("*")
            .eq("student_id", student_id)
            .execute()
        )

        if response.data:
            return response.data[0]   # Student dictionary return karega

        return None

    except Exception as e:
        print(f"Error fetching student: {e}")
        return None
    
def create_subject(subject_code,name,section,teacher_id):
    data={'subject_code' : subject_code,'name':name,'section':section,'teacher_id':teacher_id}
    response=supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subject(teacher_id):
    response=supabase.table('subjects').select('*,subject_students(count),attendence_logs(timestamp)').eq('teacher_id',teacher_id).execute()
    subjects=response.data

    for sub in subjects:
        print(sub)
        sub["Total students"] = sub.get("subject_students", [{}])[0].get("count", 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendence_logs',[])
        unique_sessions =len(set(log['timestamp'] for log in attendance))
        sub['total_classes']=unique_sessions
        

        attendance
        sub.pop('subject_students',None)
        sub.pop('attendence_logs',None)

    return subjects

def enroll_student_to_subject(student_id,subject_id):
    data={
        "student_id":student_id,
        "subject_id":subject_id
    }
    response=supabase.table("subject_students").insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id,subject_id):
    response=supabase.table('subject_students').delete().eq("student_id",student_id).eq("subject_id",subject_id).execute()
    return response.data

def get_student_subjects(student_id):
    response=supabase.table("subject_students").select("*,subjects(*)").eq("student_id",student_id).execute()
    return response.data

def get_student_attendence(student_id):
    response=supabase.table("attendence_logs").select("*,subjects(*)").eq("student_id",student_id).execute()
    return response.data

def create_attendance(attendance_to_log):
    response=supabase.table("attendence_logs").insert(attendance_to_log).execute()
    return response.data