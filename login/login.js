const listAccount = [
    {
        email: "hiep@gmail.com",
        password: "123456"
    },
    {
        email: "khanh@gmail.com",
        password: "123456"
    },
    {
        email: "ha@gmail.com",
        password: "123456"
    }
]

let isLogin = !!localStorage.getItem("token")

function CheckLogin(){
    if (isLogin){
        window.location.href = "home.html"
    } 
}

function Login(){
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let checkLogin = listAccount.some(value => value.email == email && value.password == password)
    if (checkLogin){
        localStorage.setItem("token", email)
        isLogin = true
        CheckLogin()
    } else {
        alert("Wrong email or password.")
    }
}