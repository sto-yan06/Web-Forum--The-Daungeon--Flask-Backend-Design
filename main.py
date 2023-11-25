from flask import Flask, render_template, request, redirect, url_for, session ,flash, jsonify
from cryptography.fernet import Fernet
from flask_mysqldb import MySQL
from password_utils import hash_password, verify_password
from passlib.hash import bcrypt
import os
from functools import wraps



app = Flask(__name__,template_folder="static")
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
key = Fernet.generate_key()

activity_log = []

ROLES = {
    "user": ['view_thread', 'create_thread', 'comment_thread'],
    "admin": ['view_thread', 'create_thread', 'comment_thread', 'delete_thread']
}

app.config['MYSQL_HOST'] = # YOUR PRIVATE INFO
app.config['MYSQL_USER'] = # YOUR PRIVATE INFO
app.config['MYSQL_PASSWORD'] = # YOUR PRIVATE INFO
app.config['MYSQL_DB'] = # YOUR PRIVATE INFO

app.config['THREADS_PER_PAGE'] = 3

mysql = MySQL(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


#MAIN PAGE WEATHER AUTHENTICATED OR NOT
@app.route("/")
def index():
    if session.get('authenticated'):
        return redirect(url_for('dashboard'))
    
    else:
        return render_template("home.html")


#REGISTRATION
@app.route("/registration", methods=['GET', 'POST'])
def reg():
    if request.method == "POST":
        name = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        age = request.form["age"]
        gender = request.form["gender"]
        interests = request.form["interests"]

        if(password != confirm_password):
            return "Introduced passwords do not match!" , 400
        hashed_password = hash_password(password)

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO registrationform (username, email, password, age, gender, interests) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, email, hashed_password, age, gender, interests))
        mysql.connection.commit()
        cursor.close()

        return redirect('/login')
    return render_template("registration.html")


#LOGIN ROUTE
@app.route("/login" , methods = ['GET', 'POST'])
def login():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username, password, role FROM registrationform WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()


        if user:
           # Store the original password for autofill
            session['original_password'] = password
            session['username'] = username

            #Verify the hashed password using passlib
            if bcrypt.verify(password, user[1]):
                session['authenticated'] = True
                session['role'] = user[2]

                return redirect('/forum')
            else:
                flash('Invalid username or password. Please try again', 'error')
        else:
            flash('User does not exist.Please register', 'error')
        
    return render_template("login.html")

#REQUIRING ADMIN
def has_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('authenticated'):
                user_role = session.get('role', 'user')
                if user_role == permission:
                    return f(*args, **kwargs)
                else:
                    flash("Permission denied", 'error')
                    return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))
        return decorated_function
    return decorator


#MAIN PAGE AFTER LOGIN
@app.route("/forum")
@login_required
def dashboard():
    if 'username' in session:

        page = request.args.get('page', type=int, default=1)
        page_gt = request.args.get('page_gt', type=int, default=1)

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, title, content, author, created_at FROM threads ORDER BY created_at DESC")
        threads = cursor.fetchall()
        cursor.execute("SELECT id, title, content, author, created_at FROM game_tips_threads ORDER BY created_at DESC")
        game_tips_threads = cursor.fetchall()
        cursor.close()

        #General Discussion Thread Pagination

        total_threads = len(threads)
        threads_per_page = app.config['THREADS_PER_PAGE']
        total_pages = (total_threads + threads_per_page -1) // threads_per_page

        start_idx = (page -1) * threads_per_page
        end_idx = start_idx + threads_per_page
        threads_on_page = threads[start_idx:end_idx]

        #Game Tips Discussion Thread pagination

        game_tips_total_threads = len(game_tips_threads)
        game_tips_threads_per_page = app.config['THREADS_PER_PAGE']
        game_tips_total_pages = (game_tips_total_threads + game_tips_threads_per_page -1) // game_tips_threads_per_page

        game_tips_threads_idx = (page_gt -1) * game_tips_threads_per_page
        game_tips_threads_end_idx = game_tips_threads_idx + game_tips_threads_per_page
        game_tips_threads_on_page = game_tips_threads[game_tips_threads_idx:game_tips_threads_end_idx]


        return render_template("dashboard.html", threads = threads_on_page, game_tips_threads=game_tips_threads_on_page, current_page = page, current_page_gt = page_gt,thread_total_pages = total_pages, game_tips_total_pages = game_tips_total_pages)
    else:
        return redirect('/login')
    

#LOGOUT
@app.route("/logout")
def logout():
    session.pop('username', None) #Remove username session
    session.pop('authenticated', None) # Remove autheticated session
    return redirect ('/')

#OWN PROFILE
@app.route("/forum/profile")
def profile():

    page_gd = request.args.get('page_gd', type=int, default=1)
    page_gt = request.args.get('page_gt', type=int, default=1)

    #USER INFO
    username = session.get('username')
    user_role = session.get('role')

    #DATA FETCH FOR REGISTRATION
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT profile_pic FROM registrationform WHERE username = %s", (username,))
    user_data = cursor.fetchone()
    cursor.close()
    
    #DATA FETCH FOR GAME TIPS THREADS
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, title, created_at FROM game_tips_threads WHERE author = %s", (username,))
    gametips_data = cursor.fetchall()
    cursor.close()

    #PAGINATION FOR GAMETIPS THREADS
    total_gametipsdata = len(gametips_data) # TOTAL THREADS
    total_gametipsdata_per_page = app.config['THREADS_PER_PAGE'] #THREADS PER PAGE
    total_gametipsdata_pages = (total_gametipsdata + total_gametipsdata_per_page -1) // total_gametipsdata_per_page # TOTAL PAGES
    
    total_gametips_data_idx = (page_gt -1) * total_gametipsdata_per_page #INDEX CALCULATIO
    total_gametips_data_end_idx = total_gametips_data_idx + total_gametipsdata_per_page #END INDEX CALCULATIO
    total_gametips_data_on_page = gametips_data[total_gametips_data_idx:total_gametips_data_end_idx] # TOTAL THREADS ON THE CURRENT PAGE


    #DATA FETCHED FOR NORMAL THREADS

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, title, created_at FROM threads WHERE author= %s", (username,))
    main_threads_data = cursor.fetchall()
    cursor.close()
    
    #PAGIONATION FOR GENERAL DATA THREADS

    total_general_data = len(main_threads_data) #TOTAL THREADS
    total_general_data_per_page = app.config['THREADS_PER_PAGE']  # THREADS PER PAGE
    total_general_data_pages = (total_general_data + total_general_data_per_page -1) // total_general_data_per_page #TOTAL PAGES

    total_general_data_idx = (page_gd -1) * total_general_data_per_page #INDEX CALCULATION
    total_general_data_end_idx = total_general_data_idx + total_general_data_per_page #END INDEX CALCULATION
    total_general_data_on_page = main_threads_data[total_general_data_idx:total_general_data_end_idx] #TOTAL THREADS ON THE CURRENT PAGE




    profile_pic = user_data[0] if user_data else None
    
    return render_template("user-profile.html", username = username, role = user_role, profile_pic = profile_pic, main_threads = total_general_data_on_page, gametips_thread = total_gametips_data_on_page,
                           total_pages_for_gd = total_general_data_pages, current_page_for_gd = page_gd, total_pages_for_gt = total_gametipsdata_pages, current_page_for_gt = page_gt)


#CREATE A NEW THREAD
@app.route("/forum/new-thread", methods=['GET', 'POST'])
@login_required
def create_thread():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form['content']
        author = session['username']
        category = request.form['category']

        if category == 'general_discussion':
            category_table = 'threads'
        elif category == 'game_tips':
            category_table = 'game_tips_threads'

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM registrationform WHERE username= %s", (author,))
        author_key_value = cursor.fetchone()
        cursor.close()


        cursor = mysql.connection.cursor()
        cursor.execute(f"INSERT INTO {category_table} (title, content, author, author_key) VALUES (%s, %s, %s, %s)", (title,content, author, author_key_value))
        mysql.connection.commit()
        cursor.close()

        return redirect('/forum')
    return render_template("new-thread.html")

#THREADS AND PAGINATION #AND COMMENTARIES
@app.route("/forum/topic/<string:category>/<int:topic_id>")
def topic(category, topic_id):

    if category == "general":
        table_name = "threads"
    elif category == "game_tips":
        table_name = "game_tips_threads"
    else:
        return "Invalid category provided"

    comment_author = session['username']
    user_role = session['role']


    cursor = mysql.connection.cursor()
    cursor.execute("SELECT title, content, author, created_at FROM {} WHERE id = %s".format(table_name), (topic_id,))
    topic_data =cursor.fetchone()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT opened FROM {} WHERE id = %s".format(table_name), (topic_id,))
    thread_oppened  = cursor.fetchone()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM {} WHERE id = %s".format(table_name), (topic_id,))
    thread_id  = cursor.fetchone()
    cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM {}_comments WHERE thread_id = %s".format(table_name), (thread_id[0],))
    comment_ids = cursor.fetchall()
    cursor.close()

    comment_data = []
    author_real_list = []

    for comment_id in comment_ids:

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT author, author_key FROM {}_comments WHERE id = %s".format(table_name), (comment_id[0],))
        author_real = cursor.fetchone()
        cursor.close()

        if author_real:
            comment_data.append({"comment_id":comment_id[0], "author": author_real[0], "author_key": author_real[1]})
            author_real_list.append(author_real)
        else:
            print(f"No author found for {comment_id[0]}")


    
    # Fetch comments and decryption key from the database
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT id, content, encryption_key, author_key FROM {table_name}_comments WHERE thread_id = %s", (topic_id,))
    comments_and_keys = cursor.fetchall()
    cursor.close()


    decrypted_comments = []
    for commentId, encrypted_comment, key, author_key in comments_and_keys:
        cipher_suite = Fernet(key)
        decrypted_comment = cipher_suite.decrypt(encrypted_comment).decode()
        decrypted_comments.append({"decr_comm_id": commentId, "decrypted_comment":decrypted_comment, "decr_auth_key": author_key})



    profile_pics = []

    for author_real  in author_real_list:
            
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT profile_pic FROM registrationform WHERE id = %s", (author_real[1],))
        user_data = cursor.fetchone()
        cursor.close()

        profile_pic = user_data[0] if user_data else None
        profile_pics.append(profile_pic)

    

    if topic_data:
        return render_template("topic.html", topic = topic_data,thread_oppened = thread_oppened,
                               user_role = user_role, top_id = topic_id, gd_cat = category ,decrypted_comments=decrypted_comments, 
                                profile_pict = profile_pics, comment_data=comment_data)
    else:
        return "Topic not found or doesn't exist!"
    

# PROFILE PICTURE UPLOAD
@app.route("/upload-profile-pic", methods=['POST'])
def upload_profile_pic():
    if 'profilePic' in request.files:
        profile_Pic = request.files['profilePic']
        if profile_Pic.filename != '':
            file_path = "static/profile_pictures/" + profile_Pic.filename
            profile_Pic.save(file_path)

            db_file_path = "/" + file_path

            username = session.get('username')
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE registrationform SET profile_pic = %s WHERE username = %s", (db_file_path, username))
            mysql.connection.commit()
            cursor.close()

    return redirect (url_for('profile'))


#ADMIN THINGS


@app.route("/admin-page")
@has_permission("admin")
def admin_page():
    return "Admin Page"

@app.route("/admin-page/dashboard")
@has_permission("admin")
def admin_dashboard():
    try: 
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, username, email, role FROM registrationform")
        users = cursor.fetchall()

        cursor.execute("SELECT id, title, content, author, created_at FROM threads ORDER BY created_at DESC")
        threads = cursor.fetchall()

        cursor.execute("SELECT id, title, content, author, created_at FROM game_tips_threads ORDER BY created_at DESC")
        game_tips_threads = cursor.fetchall()

        cursor.close()

        username = session.get('username')

    except Exception as e:
        return str(e)
    

    return render_template("admin_dashboard.html", users = users, threads = threads, game_threads = game_tips_threads, admin_name = username)

#USER DELETION WITH CONFIRMATION
@app.route('/admin/delete-user/<int:user_id>', methods=['GET', 'POST'])
@has_permission("admin")
def delete_user(user_id):
    if request.method == 'POST':

        # Set author_key to NULL in threads_comments
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE threads_comments SET author_key = NULL WHERE author_key = %s", (user_id,))
        mysql.connection.commit()

        # Set author_key to NULL in game_tips_threads_comments
        cursor.execute("UPDATE game_tips_threads_comments SET author_key = NULL WHERE author_key = %s", (user_id,))
        mysql.connection.commit()

        # Set author_key to NULL in threads
        cursor.execute("UPDATE threads SET author_key = NULL WHERE author_key = %s", (user_id,))
        mysql.connection.commit()

        # Set author_key to NULL in game_tips_threads
        cursor.execute("UPDATE game_tips_threads SET author_key = NULL WHERE author_key = %s", (user_id,))
        mysql.connection.commit()

        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM registrationform WHERE id = %s", (user_id, ))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    return render_template('confirm_delete_user.html', user_id=user_id)
    
#USER EDIT
@app.route('/admin/edit-user/<int:user_id>', methods=['GET', 'POST'])
@has_permission('admin')
def edit_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM registrationform WHERE id= %s", (user_id, ))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return "User not found", 400
    
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        new_role = request.form.get('role')

        if new_username is not None:
            # Update username
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE registrationform SET username = %s WHERE id = %s", (new_username, user_id))
            mysql.connection.commit()
            cursor.close()

        if new_email is not None:
            # Update email
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE registrationform SET email = %s WHERE id = %s", (new_email, user_id))
            mysql.connection.commit()
            cursor.close()

        if new_role is not None:
            # Update username
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE registrationform SET role = %s WHERE id = %s", (new_role, user_id))
            mysql.connection.commit()
            cursor.close()

        return redirect(url_for('admin_dashboard'))
    return render_template('edit_user.html', user=user)


@app.route('/add_activity', methods=['POST'])

def add_activity():
    if request.method == 'POST':
        activity = request.form.get('activity')
        if activity:
            activity_log.append(activity)
            return 'Activity added successfully'
        else:
            return "Invalid activity", 400

@app.route('/get_activity_log')
def get_activity_log():
    return jsonify(activity_log)



#Close thread ( Fetch data from database to get if thread is oppened or not)
@app.route('/forum/topic/<string:category>/<int:topic_id>/close-thread', methods = ["POST"])
def close_thread(category, topic_id):

    current_user_id = session['username']
    role = session['role']

    if category == "general":
        table_name = "threads"
    elif category == "game_tips":
        table_name = "game_tips_threads"
    else:
        return jsonify({"message": "Invalid Category provided"})

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT author, opened FROM {} WHERE id = %s".format(table_name), (topic_id,))
    result =cursor.fetchone()
    cursor.close()
    try:
        if result:
            author, thread_oppened = result

            if has_permission("admin") or (current_user_id == author):
                cursor =  mysql.connection.cursor()
                cursor.execute("UPDATE {} SET opened = 0 WHERE id = %s".format(table_name), (topic_id,))
                mysql.connection.commit()
                cursor.close()
                return jsonify({"success": True, "message": "Thread successfully closed"})
            else:
                return jsonify({"success": False, "message": "Permission denied! You must be an admin or the author of the post!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route('/forum/topic/<string:category>/<int:topic_id>/add-comment', methods=['GET', 'POST'])
def add_comment(category, topic_id):

    if category == "general":
        table_name = "threads"
    elif category == "game_tips":
        table_name = "game_tips_threads"
    else: 
        return "Invalid category provided"

    if 'username' in session: # user autenthicated 
        comment_content = request.form['comment-content']
        comment_author = session['username']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM registrationform WHERE username = %s", (comment_author,))
        user_id = cursor.fetchone()
        real_user_id = user_id[0] if user_id else None
        cursor.close()

        #ENCRYPT COMMENT
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_comment = cipher_suite.encrypt(comment_content.encode())

        cursor = mysql.connection.cursor()
        cursor.execute(f"INSERT INTO {table_name}_comments (thread_id, author, content, encryption_key, author_key) VALUES (%s, %s, %s, %s, %s)",
                       (topic_id, comment_author, encrypted_comment, key,real_user_id,))
        mysql.connection.commit()
        cursor.close()
    
        return redirect(url_for('topic', category=category, topic_id=topic_id))
    else:
        return redirect(url_for('login'))  # Redirect to the login page if the user is not authenticated.



if __name__ == "__main__":
    app.run(debug=True)

