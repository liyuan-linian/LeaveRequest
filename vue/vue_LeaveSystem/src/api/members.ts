import service from "../utils";


//这里url替换为后端登录页面url
export function login(username:string,password:string){
    return service.post('/members/login',{
        username,
        password,
    })
}