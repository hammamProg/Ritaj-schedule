from flask import Flask, render_template, request,redirect,session,url_for,flash
import io
import csv


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['USER_COUNTER'] = 0

days = ["Saturday", "Sunday","Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

hours = [7,8,9,10,11,12,13,14,15,16,17,18]

courses = []






@app.route('/', methods=['GET', 'POST'])
def show_schedule():
    if request.method == 'POST':
        # Check if the 'my_list' key exists in the session
        if 'my_list' in session:
            # If the key exists, retrieve the list from the session
            my_list = session['my_list']
        else:
            # If the key does not exist, initialize the list
            my_list = []

        print(request.data)

        course_title = request.form['courseTitle']
        slot_color = request.form['slotColor']
        meeting_days = request.form.getlist('meetingDay')
        if len(meeting_days)==0:
            flash('Please choose at least one day for course meetings!', 'fail')
            return redirect(url_for('show_schedule'))
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        instructor = request.form['instructor']
        # location = request.form['location']

        c = [course_title,[[int(num) for num in start_time.split(":")],[int(num) for num in end_time.split(":")]],meeting_days,instructor,slot_color]

        # Append the course data to the list
        my_list.append(c)
        session['my_list'] = my_list

        flash('Course Added', 'success')

        print(courses)
        return redirect(url_for('show_schedule'))
    return render_template('schedule.html', days=days, hours=hours, courses=courses)


@app.route('/clear_list')
def clear_list():
    # Clear the list in the session
    session.pop('my_list', None)
    return redirect(url_for('show_schedule'))

@app.route('/edit_course/<int:course_index>', methods=['GET', 'POST'])
def edit_course(course_index):
    if request.method == 'POST':
        course = courses[course_index]

        course['course_title'] = request.form['courseTitle']
        course['slot_color'] = request.form['slotColor']
        course['meeting_days'] = request.form.getlist('meetingDay')
        course['start_time'] = request.form['startTime']
        course['end_time'] = request.form['endTime']
        course['instructor'] = request.form['instructor']
        # location = request.form['location']

        return redirect(url_for('show_schedule'))

    return render_template('edit_course.html', course=courses[course_index])


@app.route('/delete/<int:course_index>',methods=['GET', 'POST'])
def delete_course(course_index):
    courses = session['my_list']
    courses.pop(course_index)
    session['my_list'] = courses
    flash('Course has been deleted', 'success')
    return redirect(url_for('show_schedule')) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


