from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, ReplayForm, SignupForm, SafetyForm, FieldlogForm , EmployeeForm, GroupForm
from .models import Accident, Safety, LogRecord, Manage, Fieldlog , Employee, Group
from django.db.models import Q

#회원가입
def Signup(request):
    if request.method=="GET":
        signupForm = SignupForm()
        context = {'signupForm':signupForm}
        return render(request, 'board/signup.html', context)
    
    elif request.method=="POST":
        signupForm = SignupForm(request.POST)
        if signupForm.is_valid(): #유효성 검사
            manage = signupForm.save(commit=False)
            manage.save()
        return redirect("board:login")

#로그인
def Login(request):
    if request.method == "POST":
        loginForm = AuthenticationForm(request, request.POST)
        if loginForm.is_valid():
            print("인증성공")
            auth_login(request, loginForm.get_user())
            LogRecord.objects.create(action='Login', user=request.user)
            return redirect("board:dashboard")
        else:
            print("인증실패")
            return render(request, 'board/login.html', {'error': '로그인 실패'})
    return render(request, 'board/login.html')

#로그아웃
def Logout(request):
    user = request.user.username
    auth_logout(request)
    LogRecord.objects.create(action='Logout', user=Manage.objects.get(username=user))
    return redirect("board:login")

#일일기록
class LogView(LoginRequiredMixin, ListView):
    model = LogRecord
    template_name = 'board/log.html'
    context_object_name = 'logs'

    def get_queryset(self):
        login_logs = self.model.objects.filter(action='Login').order_by('-date')
        logout_logs = self.model.objects.filter(action='Logout').order_by('-date')
        logs = []

        for logout_log in logout_logs:
            login_log = login_logs.filter(date__lt=logout_log.date).first()
            if login_log:
                duration = logout_log.date - login_log.date
                logs.append({'login': login_log, 'logout': logout_log, 'duration': duration})
                login_logs = login_logs.exclude(pk=login_log.pk)
        return logs


#사고보고 작성
class AccidentCreateView(LoginRequiredMixin,CreateView):
    model = Accident
    template_name = 'board/accident_form.html'
    form_class = PostForm
    success_url = reverse_lazy('board:accident_list')
    
    def form_valid(self, form): #사용자 인증
        form.instance.writer = self.request.user
        return super().form_valid(form)
    
#사고보고 목록
class AccidentListView(LoginRequiredMixin, ListView):
    model = Accident
    queryset = Accident.objects.all() #모델 속성 무시
    context_object_name = "accident_list"

    def get_context_data(self, **kwargs): #조회수
        context = super().get_context_data(**kwargs)
        count1 = Accident.objects.filter(ac_status='사고발생').count()
        count2  = Accident.objects.filter(ac_status='조치완료').count()
        context['count1'] = count1
        context['count2'] = count2
        context['total'] = count1 + count2
        print(f"Count: {context}")
        return context

#사고보고 확인
class AccidentDetailView(LoginRequiredMixin,DetailView):
    model = Accident
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replayForm = ReplayForm()
        context['replayForm'] = replayForm
        return context

    def post(self, request, *args, **kwargs):  # Update method signature
        replayForm = ReplayForm(request.POST)
        if replayForm.is_valid():
            replay = replayForm.save(commit=False)
            replay.writer = request.user
            post = self.get_object()
            replay.post = post
            replay.save()
        return redirect('board:accident_detail', pk=self.kwargs['pk'])
    
#사고보고 수정
class AccidentUpdateView(LoginRequiredMixin, UpdateView):
    model = Accident
    fields = "__all__"
    success_url = reverse_lazy('board:accident_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class) #업데이트 보기 객체 검색 호출
        form.fields.pop('writer', None) #작성자 지우기
        return form
    
#사고보고 삭제
class AccidentDeleteView(LoginRequiredMixin, DeleteView):
    model = Accident
    success_url = reverse_lazy('board:accident_list')

    def delete(self): # def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

#안전점검일지 작성
class SafetyCreateView(LoginRequiredMixin, CreateView):
    model = Safety
    template_name = 'board/safety_form.html'
    form_class = SafetyForm
    success_url = reverse_lazy('board:safety_list')
    
    def form_valid(self, form): #사용자 인증
        form.instance.writer = self.request.user
        return super().form_valid(form)

#안전점검일지 목록
class SafetyListView(LoginRequiredMixin, ListView):
    model = Safety
    queryset = Safety.objects.all()
    context_object_name = "safety_list"

    def get_context_data(self, **kwargs): #조회수
        context = super().get_context_data(**kwargs)
        count1 = Safety.objects.filter(scl_status='양호').count()
        count2 = Safety.objects.filter(scl_status='주의').count()
        count3 = Safety.objects.filter(scl_status='심각').count()
        context['count1'] = count1
        context['count2'] = count2
        context['count3'] = count3
        context['total'] = count1 + count2 + count3
        print(f"Count: {context}")
        return context


#안전점검일지 확인
class SafetyDetailView(LoginRequiredMixin, DetailView):
    model = Safety
    context_object_name = 'safety'  #템플릿 파일에서 사용할 컨텍스트 변수명 지정

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replayForm = ReplayForm()  # Change ReplayForm() to SafetyForm()
        context['replayForm'] = replayForm
        return context

    def post(self, request, *args, **kwargs):
        replayForm = ReplayForm(request.POST)  # Change ReplayForm() to SafetyForm()
        if replayForm.is_valid():
            replay = replayForm.save(commit=False)
            replay.writer = request.user
            safety  = self.get_object()
            replay.safety = safety
            replay.save()
        return redirect('board:safety_detail', pk=self.kwargs['pk'])
    
#안전점검일지 수정
class SafetyUpdateView(LoginRequiredMixin, UpdateView):
    model = Safety
    fields = "__all__"
    success_url = reverse_lazy('board:safety_list')

    def get_form(self, form_class=None): #?????????????
        form = super().get_form(form_class) #업데이트 보기 객체 검색 호출
        form.fields.pop('writer', None) #작성자 지우기
        return form

#안전점검일지 삭제
class SafetyDeleteView(LoginRequiredMixin, DeleteView):
    model = Safety
    success_url = reverse_lazy('board:safety_list')

    def delete(self): # def delete(self, request, *args, **kwargs):     ????????????????
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

#작업현장일지 작성, 목록
class FieldlogView(LoginRequiredMixin, CreateView, ListView):
    model = Fieldlog
    template_name = 'board/fieldlog_form.html'
    form_class = FieldlogForm
    success_url = reverse_lazy('board:fieldlog_write')  # Use reverse_lazy to avoid import errors

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)
    
#작업현장일지 확인
class FieldlogDetailView(LoginRequiredMixin, DetailView):
    model = Fieldlog
    context_object_name = 'fieldlog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replayForm = ReplayForm()
        context['replayForm'] = replayForm
        return context

    def post(self, request, *args, **kwargs):
        replayForm = ReplayForm(request.POST)
        if replayForm.is_valid():
            replay = replayForm.save(commit=False)
            replay.writer = request.user
            fieldlog  = self.get_object()
            replay.fieldlog = fieldlog
            replay.save()
        return redirect('board:fieldlog_detail', pk=self.kwargs['pk'])

#작업현장일지 수정
class FieldlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Fieldlog
    fields = "__all__"
    success_url = reverse_lazy('board:fieldlog_write')

    def get_form(self, form_class=None): #?????????????
        form = super().get_form(form_class) #업데이트 보기 객체 검색 호출
        form.fields.pop('writer', None) #작성자 지우기
        return form

#작업현장일지 삭제
class FieldlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Fieldlog
    success_url = reverse_lazy('board:fieldlog_write')

    def delete(self): # def delete(self, request, *args, **kwargs): ?
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

#직원 등록 및 목록 확인
class EmployeeView(LoginRequiredMixin, CreateView, ListView, DetailView):
    model = Employee
    template_name = 'board/employee_regi.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('board:employee')


    def get_context_data(self, **kwargs): #pytho 총 직원 수
        context = super().get_context_data(**kwargs)
        count= Employee.objects.count()
        context['count'] = count
        print(f"Count: {context}")
        employee_id = self.kwargs.get(self.pk_url_kwarg)
        if employee_id:
            context['employee'] = self.model.objects.get(pk=employee_id)
        return context
    
#직원수정
class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    fields = "__all__"
    template_name = 'board/employee_regi.html'  
    success_url = reverse_lazy('board:employee')
#직원삭제
class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('board:employee')

    def delete(self): # def delete(self, request, *args, **kwargs): ?
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())
    
# #직원합 조
# def calculate_pair(employee1, employee2):
#     return str(employee1.id) + str(employee2.id)
#근무편성
class GroupView(LoginRequiredMixin, CreateView, ListView):
    model = Group
    template_name = 'board/emp_group.html'
    form_class = GroupForm
    success_url = reverse_lazy('board:groups')

    def form_valid(self, form):
        employee1 = form.cleaned_data['employee1']
        employee2 = form.cleaned_data['employee2']

        if employee1 == employee2:
            error_message = '서로 다른 직원을 선택하세요.'
            groups = Group.objects.all()
            return render(self.request, 'board/emp_group.html', {'form': form, 'error_message': error_message, 'object_list': groups})

        existing_group = Group.objects.filter(
            Q(employee1=employee1) | Q(employee2=employee2) | Q(employee1=employee2) | Q(employee2=employee1)
        ).exists()
        if existing_group:
            error_message = '이미 편성된 조이거나 조가 있는 직원입니다.'
            # Retrieve the existing group data
            groups = Group.objects.all()
            return render(self.request, 'board/emp_group.html', {'form': form, 'error_message': error_message, 'object_list': groups})

        # form.instance.pair = calculate_pair(employee1, employee2)
        
        return super().form_valid(form)
#근무편성 삭제
class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'board/emp_group.html'  # Create a delete_group.html template for confirmation message
    success_url = reverse_lazy('board:groups')  # URL to redirect after successful deletion

    def delete(self): # def delete(self, request, *args, **kwargs): ?
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

# <a href="{% url 'board:safety_list' %}" class="nav-link">안전점검일지</a>
class DashboardView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'board/dashboard.html'
    # success_url = reverse_lazy('board:dashboard')
    context_object_name = 'dashboards'

    def get_queryset(self): #디폴트(쿼리셋 속성 반환), 쿼리셋 속성이 지정되지 않은 경우 모델 매니저 클래스의 all()메소드를 호출해 쿼리셋 객체를 생성해 반환하다.
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs): # 뷰에서 템플릿 파일에 넘겨주는 컨텍스트 데이터를 추가하거나 변경하는 목적으로 오버라이딩 한다.
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            selected_pk = self.kwargs['pk']
            selected_item = self.get_queryset().filter(pk=selected_pk).first()
            context['selected_data'] = selected_item
        else:
            context['selected_data'] = None
        return context
    
#관리자정보
class PreferencesView(LoginRequiredMixin, ListView): #리스트 디테일
    model = Manage
    template_name = 'board/preferences.html'
    context_object_name = 'preferences'

    def get_queryset(self): #디폴트(쿼리셋 속성 반환), 쿼리셋 속성이 지정되지 않은 경우 모델 매니저 클래스의 all()메소드를 호출해 쿼리셋 객체를 생성해 반환하다.
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs): # 뷰에서 템플릿 파일에 넘겨주는 컨텍스트 데이터를 추가하거나 변경하는 목적으로 오버라이딩 한다.
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            selected_pk = self.kwargs['pk']
            selected_item = self.get_queryset().filter(pk=selected_pk).first()
            context['selected_data'] = selected_item
        else:
            context['selected_data'] = None
        return context
# 부모 클래스로부터 상속받은 메서드의 내용을 재정의(변경) 하는 것을 오버라이딩이라고 한다


def Apimap(request):
    return render(request, 'board/apimap.html')