// region: add/edit/delete/view student/teacher/course/grade/attendance
const dataTypeEntryPoint = {
    attendance: "/api/attendance",
    course: "/api/course",
    grade: "/api/grade",
    student: "/api/student",
    teacher: "/api/teacher",
};

const promptInput = {
    attendance: {
        create: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            date: "Enter date (YYYY-MM-DD, leave blank for today)",
            status: "Enter attendance status (1 or 0)",
        },
        read: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            date: "Enter date (YYYY-MM-DD, leave blank for today)",
        },
        update: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            date: "Enter date (YYYY-MM-DD, leave blank for today)",
            status: "Enter attendance status (1, 0 or leave blank to flip)",
        },
        delete: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            date: "Enter date (YYYY-MM-DD, leave blank for today)",
        },
    },
    course: {
        create: {
            course_id: "Enter course ID",
            course_name: "Enter course name",
            teacher_id: "Enter teacher ID",
            credits: "Enter course credit",
        },
        read: {
            course_id: "Enter the course ID to view",
        },
        update: {
            course_id: "Enter the course ID to edit",
            course_name: "Enter new course name",
            teacher_id: "Enter new teacher ID",
            credits: "Enter new course credit",
        },
        delete: {
            course_id: "Enter the course ID to delete",
        },
    },
    grade: {
        create: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            grade: "Enter grade",
        },
        read: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
        },
        update: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
            grade: "Enter new grade",
        },
        delete: {
            student_id: "Enter student ID",
            course_id: "Enter course ID",
        },
    },
    student: {
        create: {
            student_id: "Enter student ID",
            student_name: "Enter student name",
            date_of_birth: "Enter student DOB (YYYY-MM-DD)",
            email: "Enter student email",
            phone_number: "Enter student phone number",
        },
        read: {
            student_id: "Enter the student ID to view",
        },
        update: {
            student_id: "Enter the student ID to edit",
            student_name: "Enter new student name",
            date_of_birth: "Enter new DOB (YYYY-MM-DD)",
            email: "Enter new email",
            phone_number: "Enter new phone number",
        },
        delete: {
            student_id: "Enter the student ID to delete",
        },
    },
    teacher: {
        create: {
            teacher_name: "Enter teacher name",
            teacher_id: "Enter teacher ID",
            date_of_birth: "Enter teacher DOB (YYYY-MM-DD)",
            email: "Enter teacher email",
        },
        read: {
            teacher_id: "Enter the teacher ID to view",
        },
        update: {
            teacher_id: "Enter the teacher ID to edit",
            teacher_name: "Enter new teacher name",
            date_of_birth: "Enter new DOB (YYYY-MM-DD)",
            email: "Enter new email",
        },
        delete: {
            teacher_id: "Enter the teacher ID to delete",
        },
    },
};

const createYamlPopup = async (yaml_data) => {
    const parent = document.querySelector("main");
    const popup = document.createElement("div");
    popup.classList.add("popup-container");

    const popupContent = document.createElement("div");
    popupContent.classList.add("popup-content");

    // use prismjs to generate a html code block from yaml_data
    html = `<pre class="yaml"><code>${yaml_data}</code></pre>`;

    popupContent.innerHTML = html;
    popup.appendChild(popupContent);

    const closeBtn = document.createElement("div");
    closeBtn.classList.add("btn", "btn-danger");
    closeBtn.innerHTML = "Close";

    closeBtn.addEventListener("click", () => {
        parent.removeChild(popup);
    });

    popup.appendChild(closeBtn);
    parent.appendChild(popup);
};

const takeAction = async (method, dataType) => {
    const url = dataTypeEntryPoint[dataType];
    const get_user_data = promptInput[dataType][method];
    const data = {
        action: method,
        session_key: sessionStorage.getItem("session_key"),
    };
    for (const key in get_user_data) {
        data[key] = prompt(get_user_data[key]);
        if (data[key] === null) return;
    }
    response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    const res = await response.json();
    alert(res.message);
    if (Object.keys(res.data).length !== 0)
        createYamlPopup(jsyaml.dump(res.data));
};

// endregion

// region: login/logout/register

const handler = {
    login: async () => {
        const username = prompt("Enter username");
        if (username === null) return;
        const password = prompt("Enter password");
        if (password === null) return;
        response = await fetch("/api/user/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        });
        const res = await response.json();
        alert(res.message);
        sessionStorage.setItem("session_key", res.data.session_key);
        window.location.reload();
    },
    register: async () => {
        const username = prompt("Enter username");
        if (username === null) return;
        const password = prompt("Enter password");
        if (password === null) return;
        let role = prompt(
            "Enter role of the new account (Student, Teacher or Admin)",
        );
        if (role === null) return;
        if (role === "") role = "Student";

        while (
            !["Student", "Teacher", "Admin"].includes(helper.capitalize(role))
        ) {
            alert("Role must be Student, Teacher or Admin");
            role = prompt("Enter role of the new account");
            if (role === null) return;
            if (role === "") role = "Student";
        }
        const session_key = sessionStorage.getItem("session_key");

        response = await fetch("/api/user/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
                role: helper.capitalize(role),
                session_key: session_key,
            }),
        });
        const res = await response.json();
        alert(res.message);
        window.location.reload();
    },
    logout: async () => {
        const session_key = sessionStorage.getItem("session_key");
        response = await fetch("/api/user/logout", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                session_key: session_key,
            }),
        });
        const res = await response.json();
        alert(res.message);
        sessionStorage.removeItem("session_key");
        window.location.reload();
    },
};

const createLoginOutRegBtn = (type) => {
    if (!["login", "logout", "register"].includes(type)) {
        throw new Error("Invalid button type");
    }
    const newButton = document.createElement("button");
    newButton.classList.add("btn", "btn-primary");
    newButton.innerHTML = helper.capitalize(type);
    newButton.onclick = handler[type];
    return newButton;
};

// endregion

const helper = {
    capitalize: (str) => {
        if (typeof str !== "string") return "";
        if (str.length === 0) return str;
        return str[0].toUpperCase() + str.slice(1);
    },
    isFirstUser: async () => {
        const response = await fetch("/api/user/register", { method: "GET" });
        return (await response.json()).message;
    },
    isSessionValid: async () => {
        const response = await fetch("/api/user/validate_session", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                session_key: sessionStorage.getItem("session_key"),
            }),
        });
        const res = await response.json();
        return_data = {
            isValid: response.status === 200,
            username: "",
            role: "",
        };
        if (response.status === 200) {
            return_data.username = res.data.username ? res.data.username : "";
            return_data.role = res.data.role ? res.data.role : "";
        }
        return return_data;
    },
};

// Login/logout/signup button on index page
document.addEventListener("DOMContentLoaded", async () => {
    if (sessionStorage.getItem("session_key") === null)
        sessionStorage.setItem("session_key", "");

    const element = document.querySelector(".login-welcome-signup");
    if (!element) return; // make sure the below code is only executed on the index page

    if (!sessionStorage.getItem("session_key")) {
        element.appendChild(createLoginOutRegBtn("login"));
        if (await helper.isFirstUser())
            element.appendChild(createLoginOutRegBtn("register"));
        return;
    }

    const { isValid, username, role } = await helper.isSessionValid();
    if (!isValid) {
        element.appendChild(createLoginOutRegBtn("login"));
        return;
    }

    const welcomeMsg = document.createElement("p");
    welcomeMsg.innerHTML = `Welcome ${username} (${role})`;
    element.appendChild(welcomeMsg);

    if (role === "Admin") element.appendChild(createLoginOutRegBtn("register"));
    element.appendChild(createLoginOutRegBtn("logout"));
});
