<!--/app/appView.jsp-->
<%@ page errorPage="/error.jsp" %>
<%@ page import="org.jmanage.webui.util.WebContext,
                 org.jmanage.webui.util.RequestParams,
                 java.net.URLEncoder,
                 java.util.*,
                 org.jmanage.webui.util.Utils,
                 org.jmanage.core.util.ACLConstants,
                 org.jmanage.core.management.ObjectName,
                 org.jmanage.core.config.*,
                 org.jmanage.webui.dashboard.framework.DashboardRepository,
                 org.jmanage.webui.dashboard.framework.DashboardConfig,
                 org.jmanage.webui.view.ApplicationViewHelper"%>

<%@ page import="org.jmanage.core.config.ApplicationConfig"%>
<%@ taglib uri="/WEB-INF/tags/jmanage/html.tld" prefix="jmhtml"%>
<%@ taglib uri="/WEB-INF/tags/jmanage/jm.tld" prefix="jm"%>

<script type="text/javascript" src="/js/dojo/dojo.js"></script>
<script language="JavaScript">
    function deleteAlert(alertId, appId){
        var msg;
        msg = "Are you sure you want to delete this Alert?";
        if(confirm(msg) == true){
            location = '/config/deleteAlert.do?<%=RequestParams.ALERT_ID%>=' + alertId + '&<%=RequestParams.APPLICATION_ID%>=' + appId + '&refreshApps=true';
        }
        return;
    }
    function deleteGraph(graphId, appId){
        var msg;
        msg = "Are you sure you want to delete this Graph?";
        if(confirm(msg) == true){
            location = '/config/deleteGraph.do?<%=RequestParams.GRAPH_ID%>=' + graphId + '&<%=RequestParams.APPLICATION_ID%>=' + appId + '&refreshApps=true';
        }
        return;
    }
    function deleteDashboard(dashboardID, appId){
        var msg;
        msg = "Are you sure you want to delete this Dashboard?";
        if(confirm(msg) == true){
            location = '/config/deleteDashboard.do?<%=RequestParams.DASHBOARD_ID%>='+dashboardID+'&<%=RequestParams.APPLICATION_ID%>='+appId +'&refreshApps=true';
        }
        return;
    }
</script>
<%
    WebContext webContext = WebContext.get(request);
    ApplicationConfig appConfig = webContext.getApplicationConfig();
		final String availabilityGraphURL = "/app/availabilityGraph.do?" +
		    RequestParams.APPLICATION_ID + "=" + appConfig.getApplicationId();
%>
<%-- Application Information --%>
<script type="text/JavaScript" src="/js/dashboard.js"></script>
<script type="text/JavaScript" src="/js/dojo/dojo.js.js"></script>
<div> <h3><%=appConfig.getName()%></h3></div>
<div class="row-fluid"> <!-- main div-->
    <div class="span6">
        <h4>Availability</h4>
        <img class="well" src="<%=availabilityGraphURL%>" />
        <p class="text-info">Status: <%=ApplicationViewHelper.isApplicationUp(appConfig)?"Up":"Down"%> </p>
        <p class="text-info">Recording Since: <%=ApplicationViewHelper.getRecordingSince(appConfig)%></p>
    </div>
    <div class="span6">  <!-- Start/Stop applicaiton --> 
    <table class="table">
        <thead>
            <tr>
            <th colspan="3">Operations</th>
            </tr>
        </thead>
        <form name="emptyForm" method="post" action="/app/executeOperation.do">
        <input type="hidden" name="applicationId" value=<%=appConfig.getApplicationId()%> />
        <input type="hidden" name="objName" value="Mule:name=WrapperManager"/>
        <tr>
        <td class="plaintext">
            <p>Restart</p>
        </td>
        <td>
            <input type="hidden" name="paramCount" value="0"/>
            <input type="hidden" name="operationName" value="restart"/>
            <input type="submit" value="Invoke" class="btn pull-right"/>        
        </td>
        </tr>
        </form>
        <form name="emptyForm" method="post" action="/app/executeOperation.do">
        <input type="hidden" name="applicationId" value=<%=appConfig.getApplicationId()%> />
        <input type="hidden" name="objName" value="Mule:name=WrapperManager"/>
        <tr>
        <td class="plaintext">
            <p>Stop</p>
        </td>
        <td>
            <input type="hidden" name="paramCount" value="1"/>
            <input type="hidden" name="stop0_type" value="int"/>
            <input type="hidden" name="operationName" value="stop"/>
            <input type="submit" value="Invoke" class="btn pull-right"/>
        
        </td>
         </tr>
        </form>
    </table>
    </div>
    
    <div class="row-fluid"> <%-- Configured Graphs --%>
        <%if(appConfig.getGraphs().size() > 0){%>
            <div class="span6">
        <%}else{%>
            <div class="span12">
        <%}%>    
        
        </div>

        <%if(appConfig.getGraphs().size() > 0){%>
        <div class="span6">
            
            <table class="table">
                <thead>
                <tr>
                   <th colspan="3">Graphs</th>
                </tr>
                </thead>
                <tbody>
            <%
                for(Iterator it=appConfig.getGraphs().iterator(); it.hasNext();){
                    GraphConfig graphConfig = (GraphConfig)it.next();
            %>
                <tr>
                    <td class="plaintext">
                        <a href="/app/graphView.do?<%=RequestParams.APPLICATION_ID%>=<%=appConfig.getApplicationId()%>&graphId=<%=graphConfig.getId()%>">
                                <%=graphConfig.getName()%></a>
                    </td>
                    <td align="right">
                    <%
                            String editGraphLink ="/config/showEditGraph.do?"
                                    + RequestParams.GRAPH_ID + "=" + graphConfig.getId();
                        %>
                        <jmhtml:link href="<%=editGraphLink%>" acl="<%=ACLConstants.ACL_EDIT_GRAPH%>" styleClass="btn">Edit</jmhtml:link>
                    </td>
                    <td align="right" width="30">
                    <%
                        String deleteGraphLink = "JavaScript:deleteGraph('"
                                + graphConfig.getId() + "','" + appConfig.getApplicationId() + "');";
                    %>
                        <jmhtml:link href="<%=deleteGraphLink%>" acl="<%=ACLConstants.ACL_EDIT_GRAPH%>" styleClass="btn">
                            Delete</jmhtml:link>
                   </td>
                </tr>
            <%
                }
            %>
            </tbody>
            </table>
        </div>    
            
            <%}%>
    </div>
</div>      

<div> <!-- Dashboard -->
    <table class="table table-condensed">
    <tr><td><div id="com1"><b>App up time (milliseconds) : </b>15915179</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com1', 5000, 1,'dummy','dummy')", 5000);</script>
</td><td><div id="com2"><b>Process CPU time (nanoseconds) : </b>170780000000</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com2', 5000, 1,'dummy','dummy')", 5000);</script>
</td></tr>
    <tr><td><div id="com3"><b>Total compilation time (milliseconds) : </b>38073</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com3', 5000, 1,'dummy','dummy')", 5000);</script>
</td><td>&nbsp;</td></tr>
    <tr><td colspan="2">&nbsp;</td></tr>
    <tr class="tableHeader"><td colspan="2"><a href="/config/viewDashboard.do?applicationId=1&dashBID=jvmThreads">Thread Details</a></td></tr>
    <tr><td><div id="com4"><b>Live thread count : </b>51</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com4', 5000, 1,'dummy','dummy')", 5000);</script>
</td><td><div id="com5"><b>Peak thread count : </b>71</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com5', 5000, 1,'dummy','dummy')", 5000);</script>
</td></tr>
    <tr><td><div id="com6"><b>Daemon thread count : </b>29</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com6', 5000, 1,'dummy','dummy')", 5000);</script>
</td><td><div id="com7"><b>Total number of threads started : </b>24829</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com7', 5000, 1,'dummy','dummy')", 5000);</script>
</td></tr>
    <tr class="tableHeader"><td colspan="2">Memory Details</td></tr>
    <tr><td><div id="com8"><b>Heap memory usage : </b><table class="HtmlTable"><tr><td><b>Used</b></td><td>21917 KB</td></tr><tr><td ><b>Committed</b></td><td>83008 KB</td></tr><tr><td ><b>Max</b></td><td>517760 KB</td></tr><tr><td><b>Initial</b></td><td>0 KB</td></tr></table></div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com8', 5000, 1,'dummy','dummy')", 5000);</script>
</td><td><div id="com9"><b>Non heap memory usage : </b><table class="HtmlTable"><tr><td ><b>Used</b></td><td>44163 KB</td></tr><tr><td><b>Committed</b></td><td>70328 KB</td></tr><tr><td><b>Max</b></td><td>180224 KB</td></tr><tr><td><b>Initial</b></td><td>23748 KB</td></tr></table></div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com9', 5000, 1,'dummy','dummy')", 5000);</script>
</td></tr>
    <tr><td><div id="com10"><b>Objects pending for finalization : </b>0</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com10', 5000, 1,'dummy','dummy')", 5000);</script>
</td><td>&nbsp;</td></tr>
    <tr><td colspan="2"><div id="com11"><b>Garbage collector : </b>&lt;error&gt;</div>
</td></tr>
    <tr><td colspan="2"><div id="com12"><b>Garbage collector : </b>&lt;error&gt;</div>
</td></tr>
    <tr class="tableHeader"><td colspan="2"><a href="/config/viewDashboard.do?applicationId=1&dashBID=classes">Classes</a></td></tr>
    <tr><td><div id="com13"><b>Current classes loaded : </b>5631</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com13', 5000, 1,'dummy','dummy')", 5000);</script>
</td><td><div id="com14"><b>Total classes unloaded : </b>107</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com14', 5000, 1,'dummy','dummy')", 5000);</script>
</td></tr>
    <tr><td><div id="com15"><b>Total class loaded : </b>5738</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com15', 5000, 1,'dummy','dummy')", 5000);</script>
</td><td>&nbsp;</td></tr>
    <tr><td colspan="2">&nbsp;</td></tr>
    <tr class="tableHeader"><td colspan="2">OS Details</td></tr>
    <tr><td><div id="com16"><b>Total physical memory (bytes) : </b>4294967296</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com16', 5000, 1,'dummy','dummy')", 5000);</script>
</td><td><div id="com17"><b>Free physical memory (bytes) : </b>145793024</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com17', 5000, 1,'dummy','dummy')", 5000);</script>
</td></tr>
    <tr><td><div id="com18"><b>Committed virtual memory (bytes) : </b>3535261696</div>
<script>self.setTimeout("refreshDBComponent('jvmSummary', 'com18', 5000, 1,'dummy','dummy')", 5000);</script>
</td><td>&nbsp;</td></tr>
</table>
        </div>
    </div> 
<br/>
<%-- Configured MBeans --%>

