<%@ page language="java" import="java.util.*" pageEncoding="utf-8"%>
<%
String path = request.getContextPath();
String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>My JSP 'register.jsp' starting page</title>
  </head>

  <body>
  <script type="text/javascript">
        function validate(){
            if(registerForm.uname.value==""){
                alert("账号不能为空!");
                return;
            }
            if(registerForm.upwd.value==""){
                alert("密码不能为空!");
                return;
            }
            registerForm.submit();
        }
    </script>

    <form  name="registerForm" action="DoregServlet" method="post">

        用户名:<input type="text" name="uname"><br>
        密   码: <input type="password" name="upwd"> <br>
        <input type="submit" value="注册" >
        <a href="denglu.jsp">登录</a>
    </form>

  </body>
</html>



package com.servlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.dao.UsersDao;

public class servlet3 extends HttpServlet {

    public servlet3() {
        super();
    }


    public void destroy() {
        super.destroy(); // Just puts "destroy" string in log
        // Put your code here
    }


    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost (request, response);

    }


    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String uname = request.getParameter("uname");
        String upwd = request.getParameter("upwd");
        UsersDao usersDao = new UsersDao();
        int i=usersDao.reg(uname, upwd);
        if(i>0){

            response.setHeader("refresh", "2;url=login.jsp");
        }else{

            response.setHeader("refresh", "2;url=reg.jsp");
        }
    }

    /**
     * Initialization of the servlet. <br>
     *
     * @throws ServletException if an error occurs
     */
    public void init() throws ServletException {
        // Put your code here
    }

}





package com.sf.servlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.sf.dao.MsgDao;
import com.sf.dao.UsersDao;

public class Doregservlet extends HttpServlet {

    /**
     * Constructor of the object.
     */
    public Doregservlet() {
        super();
    }

    /**
     * Destruction of the servlet. <br>
     */
    public void destroy() {
        super.destroy(); // Just puts "destroy" string in log
        // Put your code here
    }

    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        request.setCharacterEncoding("utf-8");
        String uname = request.getParameter("uname");
        String upwd = request.getParameter("upwd");

        UsersDao ud = new UsersDao();
        MsgDao md = new MsgDao();
        if (ud.register(uname, upwd) > 0) {
            request.getSession().setAttribute("uname", uname);
            request.getRequestDispatcher("denglu.jsp").forward(request,
                    response);
        } else {
            out.print("注册失败，请重新注册.......");
            response.setHeader("refresh", "3;url=reg.jsp");
        }
    }
    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        doGet(request,response);
    }

    /**
     * Initialization of the servlet. <br>
     *
     * @throws ServletException if an error occurs
     */
    public void init() throws ServletException {
        // Put your code here
    }

}





package com.servlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.dao.MsgDao;

public class servlet5 extends HttpServlet {

    public servlet5() {
        super();
    }

    public void destroy() {
        super.destroy(); // Just puts "destroy" string in log
        // Put your code here
    }


    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        doPost(request,  response);
    }


    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        request.setCharacterEncoding("utf-8");

        int id=Integer.parseInt(request.getParameter("id"));
        MsgDao md=new MsgDao();
        md.delMail(id);
        response.getWriter().print("刪除成功.....");
        response.setHeader("refresh", "2;url=main.jsp");
        response.sendRedirect("main2.jsp");
    }


    public void init() throws ServletException {

    }

}







package com.sf.servlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.sf.dao.MsgDao;
import com.sf.entity.Msg;

public class Dowriteservlet extends HttpServlet {

    /**
     * Constructor of the object.
     */
    public Dowriteservlet() {
        super();
    }

    /**
     * Destruction of the servlet. <br>
     */
    public void destroy() {
        super.destroy(); // Just puts "destroy" string in log
        // Put your code here
    }

    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        request.setCharacterEncoding("utf-8");
        String uname = (String) request.getSession().getAttribute("uname");
        String sendto = request.getParameter("receiver");
        String title = request.getParameter("title");
        String content = request.getParameter("content");

        Msg m = new Msg();
        m.setMsgcontent(content);
        m.setUsername(uname);
        m.setSendto(sendto);
        m.setTitle(title);

        MsgDao md = new MsgDao();
        md.addMsg(m);

        out.print("发送成功.....");
        response.setHeader("refresh", "3;url=main.jsp");
    }

    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        doGet(request,response);     }

    /**
     * Initialization of the servlet. <br>
     *
     * @throws ServletException if an error occurs
     */
    public void init() throws ServletException {
    }

}