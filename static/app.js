// region: add/edit/delete/view student/teacher/course/grade/attendance

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

const promptInput = {
    attendance: {
        add: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            date: "Enter date (YYYY-MM-DD, leave blank for today)",
            status: "Enter attendance status (1 or 0)",
        },
        edit: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            date: "Enter date (YYYY-MM-DD, leave blank for today)",
            status: "Enter attendance status (1, 0 or leave blank to not change)",
        },
        delete: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            date: "Enter date (YYYY-MM-DD, leave blank for today)",
        },
        view: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            date: "Enter date (YYYY-MM-DD, leave blank for today)",
        },
    },
    course: {
        add: {
            course_id: "Enter course ID",
            course_name: "Enter course name",
            teacher_id: "Enter teacher ID",
            credits: "Enter course credit",
        },
        edit: {
            course_id: "Enter the course ID to edit",
            course_name: "Enter new course name",
            teacher_id: "Enter new teacher ID",
            credits: "Enter new course credit",
        },
        delete: {
            course_id: "Enter the course ID to delete",
        },
        view: {
            course_id: "Enter the course ID to view",
        },
    },
    grade: {
        add: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            grade: "Enter grade",
        },
        edit: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            grade: "Enter new grade",
        },
        delete: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
        },
        view: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
        },
    },
    student: {
        add: {
            student_id: "Enter student ID",
            student_name: "Enter student name",
            date_of_birth: "Enter student DOB",
            email: "Enter student email",
            phone_number: "Enter student phone number",
        },
        edit: {
            student_id: "Enter the student ID to edit",
            student_name: "Enter new student name",
            date_of_birth: "Enter new DOB",
            email: "Enter new email",
            phone_number: "Enter new phone number",
        },
        delete: {
            student_id: "Enter the student ID to delete",
        },
        view: {
            student_id: "Enter the student ID to view",
        },
    },
    teacher: {
        add: {
            teacher_name: "Enter teacher name",
            teacher_id: "Enter teacher ID",
            date_of_birth: "Enter teacher DOB",
            email: "Enter teacher email",
        },
        edit: {
            teacher_id: "Enter the teacher ID to edit",
            teacher_name: "Enter new teacher name",
            date_of_birth: "Enter new DOB",
            email: "Enter new email",
        },
        delete: {
            teacher_id: "Enter the teacher ID to delete",
        },
        view: {
            teacher_id: "Enter the teacher ID to view",
        },
    },
};

const takeAction = (method, dataType) => {
    const url = dataTypeEntryPoint[dataType];
    const prompt = promptInput[dataType][method];
    const data = {};
    for (const key in prompt) {
        data[key] = window.prompt(prompt[key]);
        if (data[key] === null) return;
    }
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

const handleLoginRegister = (type) => {
    const username = prompt("Enter username");
    const password = prompt("Enter password");

    // endpoint: /api/user
    // login: POST
    // register: PUT

    const url = '/api/user';
    const options = {
        method: type === 'login' ? 'POST' : 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    };

    fetch(url, options)
        .then(res => res.json())
        .then(res => {
            window.alert(res.message);
            if (res.status.toString().startsWith('2')) {
                window.location.reload();
            }
        }
        )
        .catch(err => console.log(err));
};
