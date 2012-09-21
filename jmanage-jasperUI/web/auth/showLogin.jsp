<!--/auth/showLogin.jsp-->
<%@ page errorPage="/error.jsp" %>
<%@ taglib uri="/WEB-INF/tags/jmanage/html.tld" prefix="jmhtml"%>
<h1>Jasper Console</h1>
<jmhtml:javascript formName="loginForm" />
<jmhtml:form action="/auth/login" styleClass="form-horizontal" method="post" focus="username"
                            onsubmit="return validateLoginForm(this)" >

<jmhtml:errors />
<br/>

  <legend>Login</legend>
  <div class="control-group">
    <label class="control-label">Username</label>
    <div class="controls">
      <jmhtml:text property="username" />
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">Password</label>
    <div class="controls">
      <jmhtml:password property="password" />
    </div>
  </div>
  <div class="control-group">  
    <div class="controls">
    <jmhtml:submit styleClass="btn" value="Login" />
   </div>
  </div>

  
</jmhtml:form>
