<!--    /config/selectAlertSource.jsp  -->
<%@ page errorPage="/error.jsp" %>
<%@ page import="org.jmanage.webui.util.WebContext,
                 org.jmanage.core.config.ApplicationConfig,
                 org.jmanage.webui.util.RequestParams,
                 org.jmanage.core.config.AlertDeliveryConstants,
                 org.jmanage.core.config.AlertSourceConfig"%>

<%@ taglib uri="/WEB-INF/tags/jmanage/html.tld" prefix="jmhtml"%>

<jmhtml:form action="/config/selectAlertSourceType" method="post">

<table class="table">
<thead>
<tr class="tableHeader">
    <td>Select Alert Source</td>
</tr>
</thead>
<tbody>
<tr>
    <td class="plaintext"><jmhtml:radio property="alertSourceType"
                      value="<%=AlertSourceConfig.SOURCE_TYPE_NOTIFICATION%>"/>
                      <%=AlertSourceConfig.getSourceTypeDescription(AlertSourceConfig.SOURCE_TYPE_NOTIFICATION)%></td>
</tr>
<tr>
    <td class="plaintext"><jmhtml:radio property="alertSourceType"
                      value="<%=AlertSourceConfig.SOURCE_TYPE_GAUGE_MONITOR%>"/>
                      <%=AlertSourceConfig.getSourceTypeDescription(AlertSourceConfig.SOURCE_TYPE_GAUGE_MONITOR)%></td>
</tr>
<tr>
    <td class="plaintext"><jmhtml:radio property="alertSourceType"
                      value="<%=AlertSourceConfig.SOURCE_TYPE_STRING_MONITOR%>"/>
                      <%=AlertSourceConfig.getSourceTypeDescription(AlertSourceConfig.SOURCE_TYPE_STRING_MONITOR)%></td>
</tr>
<tr>
    <td class="plaintext"><jmhtml:radio property="alertSourceType"
                      value="<%=AlertSourceConfig.SOURCE_TYPE_APPLICATION_DOWN%>"/>
                      <%=AlertSourceConfig.getSourceTypeDescription(AlertSourceConfig.SOURCE_TYPE_APPLICATION_DOWN)%></td>
</tr>
<tr>
    <td align="center" colspan="2">
        <jmhtml:submit property="" value="Next" styleClass="btn" />
        &nbsp;&nbsp;&nbsp;
        <jmhtml:button property="" value="Cancel" onclick="JavaScript:history.back();" styleClass="btn" />
    </td>
</tr>
</tbody>
</table>
</jmhtml:form>
