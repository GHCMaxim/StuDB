const actionMethod = {
    add: 'POST',
    edit: 'PUT',
    delete: 'DELETE',
    view: 'GET'
};

const dataTypeEntryPoint = {
    attendance: '/api/attendance',
    course: '/api/course',
    grade: '/api/grade',
    student: '/api/student',
    teacher: '/api/teacher'
};

prompt()

const promptInput = {
    attendance: {
        add: () => ({
            student_id: prompt('Enter student ID'),
            course_id: prompt('Enter course ID'),
            attendance: prompt('Enter attendance (1 or 0)'),
            date: prompt('Enter date (YYYY-MM-DD, leave blank for today)')
        }),
        edit: () => ({
            student_id: prompt('Enter student ID'),
            course_id: prompt('Enter course ID'),
            date: prompt('Enter date (YYYY-MM-DD, leave blank for today)')
        }),
        delete: () => ({
            student_id: prompt('Enter student ID'),
            course_id: prompt('Enter course ID'),
            date: prompt('Enter date (YYYY-MM-DD, leave blank for today)')
        }),
        view: () => ({
            student_id: prompt('Enter student ID'),
            course_id: prompt('Enter course ID'),
            date: prompt('Enter date (YYYY-MM-DD, leave blank for today)')
        }),
    },
    course: {
        add: () => ({
            course_id: prompt('Enter course ID'),
            course_name: prompt('Enter course name'),
            course_description: prompt('Enter course description'),
            course_credit: prompt('Enter course credit')
        }),
        edit: () => ({
            course_id: prompt('Enter the course ID to edit'),
            course_name: prompt('Enter new course name'),
            course_description: prompt('Enter new course description'),
            course_credit: prompt('Enter new course credit')
        }),
        delete: () => ({
            course_id: prompt('Enter the course ID to delete')
        }),
        view: () => ({
            course_id: prompt('Enter the course ID to view')
        }),
    },
    grade: {
        add: () => ({
            student_id: prompt('Enter student ID'),
            course_id: prompt('Enter course ID'),
            grade: prompt('Enter grade')
        }),
        edit: () => ({
            student_id: prompt('Enter student ID'),
            course_id: prompt('Enter course ID'),
            grade: prompt('Enter new grade')
        }),
        delete: () => ({
            student_id: prompt('Enter student ID'),
            course_id: prompt('Enter course ID')
        }),
        view: () => ({
            student_id: prompt('Enter student ID'),
            course_id: prompt('Enter course ID')
        }),
    },
    student: {
        add: () => ({
            student_name: prompt('Enter student name'),
            student_id: prompt('Enter student ID'),
            date_of_birth: prompt('Enter student DOB'),
            email: prompt('Enter student email'),
            phone_number: prompt('Enter student phone number')
        }),
        edit: () => ({
            student_id: prompt('Enter the student ID to edit'),
            student_name: prompt('Enter new student name'),
            date_of_birth: prompt('Enter new DOB'),
            email: prompt('Enter new email'),
            phone_number: prompt('Enter new phone number')
        }),
        delete: () => ({
            student_id: prompt('Enter the student ID to delete')
        }),
        view: () => ({
            student_id: prompt('Enter the student ID to view')
        }),
    },
    teacher: {
        add: () => ({
            teacher_name: prompt('Enter teacher name'),
            teacher_id: prompt('Enter teacher ID'),
            date_of_birth: prompt('Enter teacher DOB'),
            email: prompt('Enter teacher email'),
        }),
        edit: () => ({
            teacher_id: prompt('Enter the teacher ID to edit'),
            teacher_name: prompt('Enter new teacher name'),
            date_of_birth: prompt('Enter new DOB'),
            email: prompt('Enter new email'),
        }),
        delete: () => ({
            teacher_id: prompt('Enter the teacher ID to delete')
        }),
        view: () => ({
            teacher_id: prompt('Enter the teacher ID to view')
        }),
    },
};

const takeAction = (method, dataType) => {
    const url = dataTypeEntryPoint[dataType];
    const prompt = promptInput[dataType][method];
    const data = prompt();
    const options = {
        method: actionMethod[method],
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };

    fetch(url, options)
        .then(res => res.json())
        .then(res => {
            window.alert(res.message);
            if (res.data) {
                console.log(res.data);
                window.alert("Open console to see the data");
            }
        }
        )
        .catch(err => console.log(err));
};