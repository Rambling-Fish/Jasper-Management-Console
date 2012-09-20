<!--    /config/admin.jsp  -->
<%@ page errorPage="/error.jsp" %>
<%@ taglib uri="/WEB-INF/tags/jstl/c.tld" prefix="c"%>

<table cellspacing="0" cellpadding="5" width="400" class="table">
<thead>
<tr class="tableHeader">
    <th>Administration</th>
</tr>
</thead>
<tbody>
<c:if test="${!sessionScope.authenticatedUser.externalUser}" >
<tr>
    <td class="plaintext">
        <a href="/auth/listUsers.do">User Management</a>
    </td>
</tr>
</c:if>
<tr>
    <td class="plaintext">
        <a href="/auth/showUserActivity.do">User Activity Log</a>
    </td>
</tr>
</tbody>
</table>
