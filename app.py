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
        if 'my_list' in session:
            my_list = session['my_list']
        else:
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

        course = [course_title,[[int(num) for num in start_time.split(":")],[int(num) for num in end_time.split(":")]],meeting_days,instructor,slot_color]


        # days of course
        days_course = course[2]
        # Calculate the start time and end time in minutes
        start_time_minutes = course[1][0][0] * 60 + course[1][0][1]
        end_time_minutes = course[1][1][0] * 60 + course[1][1][1]
        if start_time_minutes == end_time_minutes:
            flash("Start time and end time can't be same",'fail')
            return redirect(url_for('show_schedule'))

        # Check for overlaps with existing time slots
        overlap = False
        slot_overlaped_name = ''
        for slot in my_list:
            start_time_minutes_slot = slot[1][0][0] * 60 + slot[1][0][1]
            end_time_minutes_slot = slot[1][1][0] * 60 + slot[1][1][1]
            print(days_course)
            print(slot[2])
            print(days_course[0] not in slot[2])
            if not ((end_time_minutes <= start_time_minutes_slot or start_time_minutes >= end_time_minutes_slot) or ( days_course[0] not in slot[2] or days_course[1] not in slot[2]  ) ):
                overlap = True
                slot_overlaped_name = slot[0]
                print(overlap)
                break

        # If there is no overlap, add the course as a new time slot
        #if not overlap:
        #    my_list.append(course)
        #else:
        #    flash(f"There's Overlap with course [{slot_overlaped_name}] , Try Again !", 'warning')
        #    return redirect(url_for('show_schedule'))

        my_list.append(course)

        session['my_list'] = my_list


        flash('Course Added', 'success')
        print(courses)
        return redirect(url_for('show_schedule'))
    return render_template('schedule.html', days=days, hours=hours,current_course=[])


@app.route('/clear_list')
def clear_list():
    # Clear the list in the session
    session.pop('my_list', None)
    return redirect(url_for('show_schedule'))

@app.route('/edit_course/<int:course_index>', methods=['GET', 'POST'])
def edit_course(course_index):
    courses = session['my_list']
    if request.method == 'POST':
        if 'my_list' in session:
            my_list = session['my_list']
        else:
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

        course = [course_title,[[int(num) for num in start_time.split(":")],[int(num) for num in end_time.split(":")]],meeting_days,instructor,slot_color]


        # Calculate the start time and end time in minutes
        start_time_minutes = course[1][0][0] * 60 + course[1][0][1]
        end_time_minutes = course[1][1][0] * 60 + course[1][1][1]

        # Check for overlaps with existing time slots
        overlap = False
        slot_overlaped_name = ''
        for index,slot in enumerate(my_list):
            start_time_minutes_slot = slot[1][0][0] * 60 + slot[1][0][1]
            end_time_minutes_slot = slot[1][1][0] * 60 + slot[1][1][1]

            if index!=course_index and not (end_time_minutes <= start_time_minutes_slot or start_time_minutes >= end_time_minutes_slot):
                overlap = True
                slot_overlaped_name = slot[0]
                print(overlap)
                break

        # If there is no overlap, add the course as a new time slot
        #if not overlap:
        #    my_list[course_index]=course
        #else:
        #    flash(f"There's Overlap with course [{slot_overlaped_name}] , Try Again !", 'warning')
        #    return redirect(url_for('show_schedule'))

        my_list[course_index]=course

        session['my_list'] = my_list

        flash('Course Edited', 'success')

        print(courses)
        return redirect(url_for('show_schedule'))

    return render_template('edit.html', course=courses[course_index],course_index=course_index)


@app.route('/delete/<int:course_index>',methods=['GET', 'POST'])
def delete_course(course_index):
    courses = session['my_list']
    courses.pop(course_index)
    session['my_list'] = courses
    flash('Course has been deleted', 'success')
    return redirect(url_for('show_schedule'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


