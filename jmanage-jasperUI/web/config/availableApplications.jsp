<!--    /config/availableApplications.jsp  -->
<%@ page errorPage="/error.jsp" %>
<%@ page import="java.util.Map,
                 org.jmanage.webui.util.RequestAttributes,
                 java.util.Iterator,
                 org.jmanage.core.config.ApplicationType"%>

<%@ taglib uri="/WEB-INF/tags/jmanage/html.tld" prefix="jmhtml"%>

<script language="JavaScript">
    function setType(type){
        document.forms[0].type.value=type;
        document.forms[0].submit();
    }
</script>

<jmhtml:form action="/config/showAddApplication.do" method="post">
    <jmhtml:hidden property="type" value="" />
</jmhtml:form>
<table class="table">
  <thead>
<tr class="tableHeader">
    <th>Select Application Type</th>
</tr>
</thead>
<tbody>

<%
    Map applications = (Map)request.getAttribute(RequestAttributes.AVAILABLE_APPLICATIONS);
    Iterator iterator = applications.values().iterator();
    while(iterator.hasNext()){
        ApplicationType applicationType = (ApplicationType)iterator.next();
%>
  <tr>
    <td class="plaintext">
        <a href="javascript:setType('<%=applicationType.getId()%>');"><b><%=applicationType.getName()%></b></a>
    </td>
  </tr>
  <%}//while ends %>
  </tbody>
</table>
