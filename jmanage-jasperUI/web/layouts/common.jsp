<!-- /layouts/common.jsp -->
<%@ taglib uri="/WEB-INF/tags/jmanage/html.tld" prefix="jmhtml"%>
<%@ taglib uri="/WEB-INF/tags/struts/struts-tiles.tld" prefix="tiles" %>

<!DOCTYPE html>
<html lang="en">
  	<head>
	    <meta charset="utf-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <meta name="description" content="">
	    <meta name="author" content="">    
	    <!--<link href="/css/styles.css" rel="stylesheet" type="text/css" /> -->
	    <link href="/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
	    <style>
	      body {
	        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
	      }
	    </style>
	    <link href="/css/bootstrap-responsive.min.css" rel="stylesheet" type="text/css" />
	    <link href="/css/custom.css" rel="stylesheet" type="text/css" />
		<!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
	    <!--[if lt IE 9]>
	      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
	    <![endif]-->

	    <!-- Le fav and touch icons -->
	    <link rel="shortcut icon" href="../assets/ico/favicon.ico">
	    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="../assets/ico/apple-touch-icon-144-precomposed.png">
	    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="../assets/ico/apple-touch-icon-114-precomposed.png">
	    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="../assets/ico/apple-touch-icon-72-precomposed.png">
	    <link rel="apple-touch-icon-precomposed" href="../assets/ico/apple-touch-icon-57-precomposed.png">

	    <title><tiles:getAsString name="title" /></title>
	</head>
<body>

<tiles:insert attribute="header" />

<div class="container">
<tiles:insert attribute="body.header" />
<tiles:insert attribute="body.main" />

<footer>
	<tiles:insert attribute="footer" />
</footer>

</div> <!-- /container -->
</body>
</html>