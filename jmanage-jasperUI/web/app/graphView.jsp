<!--/app/graphView.jsp-->
<%@ page errorPage="/error.jsp" %>
<%@ taglib uri="/WEB-INF/tags/jmanage/jm.tld" prefix="jm"%>

<p class="well">
<jm:graph id='<%=request.getParameter("graphId")%>' />
</p>
