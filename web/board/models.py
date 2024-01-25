from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
#Manage + User = 회원가입, 로그인
class Manage(AbstractUser):
    STATUS = {
        ('감독','감독'),
        ('관리자','관리자'),
        ('반장','반장'),
    }
    position = models.CharField(max_length=30, choices=STATUS, null=True)
    address = models.CharField(max_length=200)
    call = models.CharField(max_length=20)

#로그기록
class LogRecord(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)
    user = models.ForeignKey(Manage, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.date} - {self.action} - {self.user.username}"
    
#사고보고
class Accident(models.Model):
    STATUS = {
        ('사고발생','사고발생'),
        ('조치 중','조치 중'),
        ('조치완료','조치완료'),
    }
    ac_area = models.CharField(max_length=50)
    ac_status = models.CharField(max_length=30, choices=STATUS, null=True)
    img = models.ImageField()
    ac_cont = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(Manage, on_delete=models.CASCADE)   #python manage.py createsuperuser   Manage Table

#안전점검일지
class Safety(models.Model):
    STATUS = {
        ('양호','양호'),
        ('주의','주의'),
        ('심각','심각'),
    }
    scl_area = models.CharField(max_length=50) #제목
    scl_status = models.CharField(max_length=30, choices=STATUS, null=True) #안전상태
    img = models.ImageField() #이미지
    scl_cont = models.TextField(null=True) # 내용
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(Manage, on_delete=models.CASCADE)   #작성자

#작업현장일지
class Fieldlog(models.Model):
    fl_area = models.CharField(max_length=100) #공사구역
    fl_status = models.CharField(max_length=100) #작업내역
    img = models.ImageField()
    fl_cont = models.TextField(null=True) #일지내용
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(Manage, on_delete=models.CASCADE) # 로그인 작성자
# # cmp = models.CharField(max_length=100) #회사

#댓글
class Replay(models.Model):  
    contents = models.TextField()
    create_date= models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(Manage, on_delete=models.CASCADE) # 로그인 작성자
    post = models.ForeignKey(Accident, on_delete=models.CASCADE, null=True)
    fieldlog = models.ForeignKey(Fieldlog, on_delete=models.CASCADE, null=True)
    safety = models.ForeignKey(Safety, on_delete=models.CASCADE, null=True)
    #연결될 참조키 테이블, 불러오는 건 그 데이터값만 HTML에

# zip_code=models.IntegerField()
#직원
class Employee(models.Model): #pk 자동 생성
    STATUS = {
        ('감독','감독'),
        ('관리자','관리자'),
        ('반장','반장'),
    }
    cmp = models.CharField(max_length=40)
    emp_name = models.CharField(max_length=20)
    position = models.CharField(max_length=30, choices=STATUS, null=True)
    work = models.CharField(max_length=20)
    emp_call = models.CharField(max_length=20)
    date_of_birth = models.DateField(blank=True, null=True)
    address=models.CharField(max_length=200) #상세주소
    img = models.ImageField() #증명사진
    work_area = models.CharField(max_length=100) #담당구역
    start_time = models.DateField(blank=True, null=True) #작업 시작일
    end_time = models.DateField(blank=True, null=True) #작업 끝나는일
    create_date = models.DateTimeField(auto_now_add=True) #생성일
    update_date = models.DateTimeField(auto_now=True) #수정일
    serial_num = models.CharField(max_length=100) #단말기 시리얼넘버

#근무편성
class Group(models.Model):
    employee1 = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='group_employee1')
    employee2 = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='group_employee2')
    pair = models.IntegerField(null=True)
    
#입력은 직원에서 받는다. 그러면 직원을 웨어러블에 연결한다. 그리고 일대일로 가야한다
#웨어러블
class Wearable(models.Model):
    SIGN={
        (0, '체결'),
        (1, '미체결'),
        (2, '불량체결'),
    }
    STATUS = {
    (0, '양호'),
    (1, '관심'),
    (2, '주의'),
    (3, '경계'),
    (4, '심각'),
    }
    # serial_num = models.OneToOneField(Employee, on_delete=models.CASCADE) #일대일
    hook = models.IntegerField(choices=SIGN, null=True) #안전고리
    altitude = models.FloatField() #고도
    battery = models.IntegerField(null=True)#배터리
    degree_safety = models.IntegerField(choices=STATUS, null=True) #안전도
    event = models.IntegerField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    # safe_cap = models.CharField(max_length=20)
    # safe_wch = models.CharField(max_length=20)
    # safe_tag = models.CharField(max_length=20)
