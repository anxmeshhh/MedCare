from django.shortcuts import render, redirect
from django.contrib import messages
import MySQLdb

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # ✅ Connect to MySQL directly
            db = MySQLdb.connect(
                host="shinkansen.proxy.rlwy.net",         # MySQL host
                user="root",              # MySQL username
                passwd="FVmxAfEiXKongXjKDVQSVlQmcHdmqvDn",   # MySQL password
                db="railway",
                port=57741  
                          # Database name
            )
            cursor = db.cursor()

            # ✅ Check if user already exists
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user:
                messages.success(request, 'Welcome back!')
                db.close()
                return redirect('dashboard')

            # ✅ If user doesn't exist → Create new entry
            query = "INSERT INTO users (email, password) VALUES (%s, %s)"
            cursor.execute(query, (email, password))
            db.commit()

            messages.success(request, 'Account created successfully!')
            db.close()
            return redirect('dashboard')

        except MySQLdb.IntegrityError:
            messages.error(request, 'User with this email already exists.')
            db.rollback()
            db.close()

        except MySQLdb.Error as e:
            messages.error(request, f"Database error: {e}")
            db.rollback()
            db.close()

    return render(request, 'users/login.html')

def dashboard_view(request):
    return render(request, 'users/dashboard.html')

def redirect_to_login(request):
    return redirect('login')
