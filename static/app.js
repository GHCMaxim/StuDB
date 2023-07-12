const requestStructure = {
    student: {
        url: '/api/student',
        add: {
            method: 'POST',
            composeData: () => ({
                student_name: window.prompt('Enter student name'),
                student_id: window.prompt('Enter student ID'),
                date_of_birth: window.prompt('Enter student DOB'),
                email: window.prompt('Enter student email'),
                phone_number: window.prompt('Enter student phone number')
            })
        },
        edit: {
            method: 'PUT',
            composeData: () => ({
                student_id: window.prompt('Enter the student ID to edit'),
                student_name: window.prompt('Enter new student name'),
                date_of_birth: window.prompt('Enter new DOB'),
                email: window.prompt('Enter new email'),
                phone_number: window.prompt('Enter new phone number')
            })
        },
        delete: {
            method: 'DELETE',
            composeData: () => ({
                student_id: window.prompt('Enter the student ID to delete')
            })
        },
        view: {
            method: 'GET',
            composeData: () => ({
                student_id: window.prompt('Enter the student ID to view')
            })
        },
    },
    course: {
        url: '/api/course',
        add: {
            method: 'POST',
            composeData: () => ({
                course_id: window.prompt('Enter course ID'),
                course_name: window.prompt('Enter course name'),
                course_description: window.prompt('Enter course description'),
                course_credit: window.prompt('Enter course credit')
            })
        },
        edit: {
            method: 'PUT',
            composeData: () => ({
                course_id: window.prompt('Enter the course ID to edit'),
                course_name: window.prompt('Enter new course name'),
                course_description: window.prompt('Enter new course description'),
                course_credit: window.prompt('Enter new course credit')
            })
        },
        delete: {
            method: 'DELETE',
            composeData: () => ({
                course_id: window.prompt('Enter the course ID to delete')
            })
        },
        view: {
            method: 'GET',
            composeData: () => ({
                course_id: window.prompt('Enter the course ID to view')
            })
        },
    },
    attendance: {
        url: '/api/attendance',
        add: {
            method: 'POST',
            composeData: () => ({
                student_id: window.prompt('Enter student ID'),
                course_id: window.prompt('Enter course ID'),
                attendance: window.prompt('Enter attendance (1 or 0)'),
                date: window.prompt('Enter date (YYYY-MM-DD, leave blank for today)')
            })
        },
        edit: {
            method: 'PUT',
            composeData: () => ({
                student_id: window.prompt('Enter student ID'),
                course_id: window.prompt('Enter course ID'),
                date: window.prompt('Enter date (YYYY-MM-DD, leave blank for today)')
            })
        },
        delete: {
            method: 'DELETE',
            composeData: () => ({
                student_id: window.prompt('Enter student ID'),
                course_id: window.prompt('Enter course ID'),
                date: window.prompt('Enter date (YYYY-MM-DD, leave blank for today)')
            })
        },
        view: {
            method: 'GET',
            composeData: () => ({
                student_id: window.prompt('Enter student ID'),
                course_id: window.prompt('Enter course ID'),
                date: window.prompt('Enter date (YYYY-MM-DD, leave blank for today)')
            })
        },
    },
};