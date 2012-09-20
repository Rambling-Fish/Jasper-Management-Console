<%@ taglib uri="/WEB-INF/tags/jmanage/html.tld" prefix="jmhtml"%>

<%
    User user = WebContext.get(request).getUser();
%>

<%@page import="org.jmanage.webui.view.UserViewHelper,
				org.jmanage.webui.util.WebContext,
                org.jmanage.core.auth.User"%>
        <%if(user != null){%>
        <div class="navbar navbar-inverse navbar-fixed-top">
          <div class="navbar-inner">
            <div class="container">
              <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </a>
              <a class="brand" href="/config/managedApplications.do">Jasper Console</a>
              <div class="nav-collapse collapse">
                <ul class="nav">
                  
                  <li><a href="/auth/profile.do">Profile</a></li>
                  <%if(UserViewHelper.hasAdminAccess(request)){ %>
                        <li><a href="/config/admin.do">Admin</a></li>
                    <%}%>
                    <li><a href="/auth/logout.do">Logout</a></li>
                    
                    <%}else{%>
                        &nbsp;
                    <%}%>
                </ul>
                    <%if(user != null){%>
                    <p class="navbar-text pull-right">
                      Logged in as <a href="/auth/profile.do"><%=user.getName()%></a>
                    </p>
                    <%}%>
              </div><!--/.nav-collapse -->
            </div>
          </div>
        </div>