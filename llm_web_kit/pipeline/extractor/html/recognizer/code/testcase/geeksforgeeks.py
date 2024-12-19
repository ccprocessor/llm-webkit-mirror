html = """
<!DOCTYPE html>
<!--[if IE 7]>
<html class="ie ie7" lang="en-US" prefix="og: http://ogp.me/ns#">
<![endif]-->
<!--[if IE 8]>
<html class="ie ie8" lang="en-US" prefix="og: http://ogp.me/ns#">
<![endif]-->
<!--[if !(IE 7) | !(IE 8)  ]><!-->
<html lang="en-US" prefix="og: http://ogp.me/ns#" >

<!--<![endif]-->
<head>
<meta charset="UTF-8" />

<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=3.0"> 
<link rel="shortcut icon" href="https://media.geeksforgeeks.org/wp-content/cdn-uploads/gfg_favicon.png" type="image/x-icon" />

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>


<meta name="theme-color" content="#308D46" />
<meta name='robots' content='index, follow, max-image-preview:large, max-snippet:-1' />

<meta name="image" property="og:image" content="https://media.geeksforgeeks.org/wp-content/cdn-uploads/gfg_200x200-min.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="200">
<meta property="og:image:height" content="200">
<meta name="facebook-domain-verification" content="xo7t4ve2wn3ywfkjdvwbrk01pvdond" />

<meta property="og:title" content="Output of Java Program | Set 7 - GeeksforGeeks" />
<meta name="description" content="A Computer Science portal for geeks. It contains well written, well thought and well explained computer science and programming articles, quizzes and practice/competitive programming/company interview Questions." />
<meta property="og:url" content="https://www.geeksforgeeks.org/output-java-program-set-7/" />
<meta name="keywords" content="Data Structures, Algorithms, Python, Java, C, C++, JavaScript, Android Development, SQL, Data Science, Machine Learning, PHP, Web Development, System Design, Tutorial, Technical Blogs, Interview Experience, Interview Preparation, Programming, Competitive Programming, Jobs, Coding Contests, GATE CSE, HTML, CSS, React, NodeJS, Placement, Aptitude, Quiz, Computer Science, Programming Examples, GeeksforGeeks Courses, Puzzles, SSC, Banking, UPSC, Commerce, Finance, CBSE, School, k12, General Knowledge, News, Mathematics, Exams" />
<meta property="og:site_name" content="GeeksforGeeks" />
<meta property="og:image" content="http://www.geeksforgeeks.org/wp-content/uploads/gfg_200X200-1.png" />
<meta property="article:section" content="Java" />
<meta property="og:type" content="article" />
<meta property="og:locale" content="en_US" />
<meta property="article:published_time" content="2016-11-07 18:29:48+00:00" />
<meta property="article:modified_time" content="2021-06-28 17:51:51+00:00" />
<meta property="og:updated_time" content="2021-06-28 17:51:51+00:00" />
<meta property="og:image:secure_url" content="http://www.geeksforgeeks.org/wp-content/uploads/gfg_200X200-1.png" />
<meta property="og:description" content="A Computer Science portal for geeks. It contains well written, well thought and well explained computer science and programming articles, quizzes and practice/competitive programming/company interview Questions." />
<script src="https://cdnads.geeksforgeeks.org/synchronously_gfg_ads.min.js"></script>
<script defer src="https://apis.google.com/js/platform.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/require.js/2.1.14/require.min.js"></script>
<!-- Removed the below script from here to prevent loading google translate js at initial load
<script async src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script> -->

<!-- FIXME:-  To be finalised whether we need to put this gpt script in header or footer  -->
<!-- //gpt.js script -->
<!-- <script async src='https://www.googletagservices.com/tag/js/gpt.js'></script> -->
<script>
   var IHPWT={}; //Initialize Namespace
  var pbjs = pbjs || {};
  pbjs.que = pbjs.que || [];
  var googletag = googletag || {};
  googletag.cmd = googletag.cmd || [];
  var gptRan = false;
</script>
<script defer src="https://ads.pubmatic.com/AdServer/js/pwt/162080/12331/pwt.js"></script>
      <script defer src="https://securepubads.g.doubleclick.net/tag/js/gpt.js"></script>
  <script defer src="https://cdnads.geeksforgeeks.org/prebid.js?ver=0.1"></script>
<script defer src="https://cdnads.geeksforgeeks.org/gfg_ads.min.js?ver=0.1"></script>

<!-- gfg tabs compatablity bundled js -->

<title>Output of Java Program | Set 7 - GeeksforGeeks</title>
<link rel="profile" href="http://gmpg.org/xfn/11" />
<link rel="pingback" href="" />
<!--[if lt IE 9]>
<script src="https://www.geeksforgeeks.org/wp-content/themes/iconic-one/js/html5.js" type="text/javascript"></script>
<![endif]-->


<!-- Video Schema for posts only -->

<!-- adding article schema markup -->


<!--POST SCHEMA through API-->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "id": "https://www.geeksforgeeks.org/output-java-program-set-7/"
  },
  "headline": "Output of Java Program | Set 7",
  "datePublished": "2016-11-07 06:29:48",
  "dateModified": "2021-06-28 05:51:51",
  "image": {
    "@type": "ImageObject",
    "url": "https://media.geeksforgeeks.org/wp-content/uploads/gfg_200X200-100x100.png",
    "width": "100",
    "height": "100"
  },
  "author": {
    "@type": "Organization",
    "name": "GeeksforGeeks",
    "url": "https://www.geeksforgeeks.org/",
    "logo": {
      "@type": "ImageObject",
      "url": "https://media.geeksforgeeks.org/wp-content/cdn-uploads/logo-new-2.svg",
      "width": "301",
      "height": "40"
    }
  },
  "publisher": {
    "@type": "Organization",
    "name": "GeeksforGeeks",
    "url": "https://www.geeksforgeeks.org/",
    "logo": {
      "@type": "ImageObject",
      "url": "https://media.geeksforgeeks.org/wp-content/cdn-uploads/logo-new-2.svg",
      "width": "301",
      "height": "40"
    }
  },
  "description": "Difficulty level : Intermediate Predict the output of following Java Programs. Program 1 : Java public class Calculator { int num = 100; public void calc(int num) { this.num = num * 10; } public void printNum() { System.out.println(num); } public static void main(String[] args) { Calculator obj = new",
  "about": [
    {
      "@type": "Thing",
      "name": "Java"
    }
  ]
}</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "url": "https://www.geeksforgeeks.org/",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://www.geeksforgeeks.org/search/{search_term_string}/",
    "query-input": "required name=search_term_string"
  }
}</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "GeeksforGeeks",
  "url": "https://www.geeksforgeeks.org/",
  "logo": "https://media.geeksforgeeks.org/wp-content/cdn-uploads/20200817185016/gfg_complete_logo_2x-min.png",
  "description": "A computer science portal for geeks. It contains well written, well thought and well explained computer science and programming articles, quizzes and practice/competitive programming/company interview Questions.",
  "founder": [
    {
      "@type": "Person",
      "name": "Sandeep Jain",
      "url": "https://in.linkedin.com/in/sandeep-jain-b3940815"
    }
  ],
  "sameAs": [
    "https://www.facebook.com/geeksforgeeks.org/",
    "https://twitter.com/geeksforgeeks",
    "https://www.linkedin.com/company/1299009",
    "https://www.youtube.com/geeksforgeeksvideos/"
  ]
}</script>

<script>
    var arrPostCat = new Array();
    var arrPostCatName="Java";
            arrPostCat.push('2058');
        var tIds = "2058";
    var termsNames = "Java,ProgrammingLanguage";
    var tIdsInclusiveParents = "2058,2056"
    var domain = 1;
    var arrPost = new Array();
    var post_id = "139720";
    var post_type = "post";
    var post_slug = window.location.href;
    var ip = "64.252.71.17";
    var post_title = `Output of Java Program | Set 7`;
    var post_status = "publish";
    var practiceAPIURL="https://practiceapi.geeksforgeeks.org/";
    var practiceURL="https://practice.geeksforgeeks.org/";
    var post_date = "2016-11-07 18:29:48";
    var commentSysUrl = "https://discuss.geeksforgeeks.org/commentEmbedV2.js";
    //var postAdApiUrlString = "";
    var link_on_code_run = '';
    var link_search_modal_top = '';
    var country_code_cf = "DE";
    
    
        var postAdApiUrlString = '2056/2058/';
</script>




<!-- This site is optimized with the Yoast SEO plugin v7.6 - https://yoast.com/wordpress/plugins/seo/ -->
<link rel="canonical" href="https://www.geeksforgeeks.org/output-java-program-set-7/" />
<script type='application/ld+json'>{"@context":"https:\/\/schema.org","@type":"Organization","url":"https:\/\/www.geeksforgeeks.org\/","sameAs":[],"@id":"https:\/\/www.geeksforgeeks.org\/#organization","name":"GeeksforGeeks","logo":"http:\/\/www.geeksforgeeks.org\/wp-content\/uploads\/gfg_200X200-1.png"}</script>
<!-- / Yoast SEO plugin. -->

<link rel='dns-prefetch' href='//www.geeksforgeeks.org' />
<link rel='dns-prefetch' href='//s.w.org' />
		<script type="text/javascript">
			window._wpemojiSettings = {"baseUrl":"https:\/\/s.w.org\/images\/core\/emoji\/11\/72x72\/","ext":".png","svgUrl":"https:\/\/s.w.org\/images\/core\/emoji\/11\/svg\/","svgExt":".svg","source":{"concatemoji":"https:\/\/www.geeksforgeeks.org\/wp-includes\/js\/wp-emoji-release.min.js?ver=4.9.8"}};
			!function(a,b,c){function d(a,b){var c=String.fromCharCode;l.clearRect(0,0,k.width,k.height),l.fillText(c.apply(this,a),0,0);var d=k.toDataURL();l.clearRect(0,0,k.width,k.height),l.fillText(c.apply(this,b),0,0);var e=k.toDataURL();return d===e}function e(a){var b;if(!l||!l.fillText)return!1;switch(l.textBaseline="top",l.font="600 32px Arial",a){case"flag":return!(b=d([55356,56826,55356,56819],[55356,56826,8203,55356,56819]))&&(b=d([55356,57332,56128,56423,56128,56418,56128,56421,56128,56430,56128,56423,56128,56447],[55356,57332,8203,56128,56423,8203,56128,56418,8203,56128,56421,8203,56128,56430,8203,56128,56423,8203,56128,56447]),!b);case"emoji":return b=d([55358,56760,9792,65039],[55358,56760,8203,9792,65039]),!b}return!1}function f(a){var c=b.createElement("script");c.src=a,c.defer=c.type="text/javascript",b.getElementsByTagName("head")[0].appendChild(c)}var g,h,i,j,k=b.createElement("canvas"),l=k.getContext&&k.getContext("2d");for(j=Array("flag","emoji"),c.supports={everything:!0,everythingExceptFlag:!0},i=0;i<j.length;i++)c.supports[j[i]]=e(j[i]),c.supports.everything=c.supports.everything&&c.supports[j[i]],"flag"!==j[i]&&(c.supports.everythingExceptFlag=c.supports.everythingExceptFlag&&c.supports[j[i]]);c.supports.everythingExceptFlag=c.supports.everythingExceptFlag&&!c.supports.flag,c.DOMReady=!1,c.readyCallback=function(){c.DOMReady=!0},c.supports.everything||(h=function(){c.readyCallback()},b.addEventListener?(b.addEventListener("DOMContentLoaded",h,!1),a.addEventListener("load",h,!1)):(a.attachEvent("onload",h),b.attachEvent("onreadystatechange",function(){"complete"===b.readyState&&c.readyCallback()})),g=c.source||{},g.concatemoji?f(g.concatemoji):g.wpemoji&&g.twemoji&&(f(g.twemoji),f(g.wpemoji)))}(window,document,window._wpemojiSettings);
		</script>
		<style type="text/css">
img.wp-smiley,
img.emoji {
	display: inline !important;
	border: none !important;
	box-shadow: none !important;
	height: 1em !important;
	width: 1em !important;
	margin: 0 .07em !important;
	vertical-align: -0.1em !important;
	background: none !important;
	padding: 0 !important;
}
</style>
<link rel='stylesheet' id='custom-style-css'  href='https://www.geeksforgeeks.org/wp-content/themes/iconic-one/css/gfg.min.css?ver=11.75' type='text/css' media='all' />
<script type='text/javascript' src='https://code.jquery.com/jquery-3.7.1.min.js?ver=3.7.1'></script>
<script type='text/javascript' src='https://code.jquery.com/jquery-migrate-3.5.2.min.js?ver=3.5.2'></script>
<script type='text/javascript'>
/* <![CDATA[ */
var gfgObject = {"authUrl":"https:\/\/auth.geeksforgeeks.org\/","writeApiUrl":"https:\/\/apiwrite.geeksforgeeks.org\/","writeUrl":"https:\/\/write.geeksforgeeks.org\/","utilUrl":"https:\/\/util.geeksforgeeks.org\/","apiUrl":"https:\/\/api.geeksforgeeks.org\/","cfApiUrl":"https:\/\/gfgapi.geeksforgeeks.org\/","baseCompilerURL":"https:\/\/codejudge.geeksforgeeks.org\/","idePageBaseUrl":"https:\/\/ide.geeksforgeeks.org\/","gfgApiScriptUrl":"https:\/\/apiscript.geeksforgeeks.org\/","gfgSiteUrl":"https:\/\/www.geeksforgeeks.org\/","curatedListId":"1","curatedListTitle":"SDE Sheet Problems","utilDjangoCfUrl":"https:\/\/utilapi.geeksforgeeks.org\/","premiumCheckoutSlug":"premium-plans-payment\/","premiumLandingSlug":"premium-plans\/","premiumCssUrl":"https:\/\/www.geeksforgeeks.org\/wp-content\/themes\/iconic-one\/css\/gfgpremium.min.css?ver=1.6","premiumJsUrl":"https:\/\/www.geeksforgeeks.org\/wp-content\/themes\/iconic-one\/js\/gfgpremium.min.js?ver=1.5","utilGoogleUrl":"https:\/\/ugprod.geeksforgeeks.org\/","communityApiUrl":"https:\/\/communityapi.geeksforgeeks.org\/","utilDjangoUrl":"https:\/\/gfgutil.geeksforgeeks.org\/","gfgPracticeUrl":"https:\/\/practiceapi.geeksforgeeks.org\/","gfgMediaUrl":"https:\/\/media.geeksforgeeks.org\/","authDjangoApiUrl":"https:\/\/authapi.geeksforgeeks.org\/","gfgMlApiUrl":"https:\/\/recommendations.geeksforgeeks.org\/","is_home":"","is_category":"","userlevelPremiumPlus":"2","practiceUrl":"https:\/\/practice.geeksforgeeks.org\/","gfgNotificationsApiUrl":"https:\/\/notificationsapi.geeksforgeeks.org\/"};
/* ]]> */
</script>
<script type='text/javascript' async="async" src='https://www.geeksforgeeks.org/wp-content/themes/iconic-one/js/gfg.min.js?ver=13.44'></script>

<link rel='shortlink' href='https://www.geeksforgeeks.org/?p=139720' />
<style>
#wpadminbar{
background: #ff0000 !important;
}
</style>
<style type="text/css" id="custom-background-css">
body.custom-background { background-color: #ffffff; }
</style>
<link rel="icon" href="https://www.geeksforgeeks.org/wp-content/uploads/gfg_200X200-100x100.png" sizes="32x32" />
<link rel="icon" href="https://www.geeksforgeeks.org/wp-content/uploads/gfg_200X200.png" sizes="192x192" />
<link rel="apple-touch-icon-precomposed" href="https://www.geeksforgeeks.org/wp-content/uploads/gfg_200X200.png" />
<meta name="msapplication-TileImage" content="https://www.geeksforgeeks.org/wp-content/uploads/gfg_200X200.png" />

<!--
<script type='text/javascript'>
  var googletag = googletag || {};
  googletag.cmd = googletag.cmd || [];
  (function() {
    var gads = document.createElement('script');
    gads.async = true;
    gads.type = 'text/javascript';
    var useSSL = 'https:' == document.location.protocol;
    gads.src = (useSSL ? 'https:' : 'http:') +
      '//www.googletagservices.com/tag/js/gpt.js';
    var node = document.getElementsByTagName('script')[0];
    node.parentNode.insertBefore(gads, node);
  })();
</script>

 AutoAds
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<script>
(adsbygoogle = window.adsbygoogle || []).push({
google_ad_client: "ca-pub-9465609616171866",
enable_page_level_ads: true
});
</script>
-->




<style>

    #internal-promo-section{
        display: none !important;
    }
    @media screen and (max-width:1500px) and (min-width:1280px){
        body.single .article-page_flex .leftBar {
            flex-basis: calc(100% - 605px);
            max-width: calc(100% - 605px);
            min-width: calc(100% - 605px);
        }
        
        .sidebar_wrapper{
            max-width: 300px;
            min-width: 300px;
        }
        
        div#secondary {
            min-width: 300px;
            max-width: 300px;
        }
        
        .widget-area{
            padding: 0px;
        }
        
        .article-page_flex .rightBar{
            padding: 20px 0px 0px 0px;
        }
        
        .article--viewer_content .a-wrapper .content {
            padding: 0px 10px 55px 20px;
        }
        
        .oinLeftbar {
            height: calc(100vh - 350px) !important;
        }  
    }
    .autoLeftBar_oin_child{
        height: 100% !important;
    }
    .autoLeftBar_oin_non_sticky{
        height: unset !important;
    }
    .sideBar--wrap.newLeftbar > div[id^='GFG_AD_Leftsidebar_']:nth-of-type(1){
        padding-top: 20px;
    }
    .sideBar--wrap.newLeftbar > div[id^='GFG_AD_Leftsidebar_']{
        padding: 5px 0;
    }

@media (max-width:1043px) and (min-width:992px) {
 .hide-1043992 {
   display: none!important;
 }
}

.mobile-header-list-item{
    padding-left:30px; 
    padding-right:10px;
    margin-top:5px;
}

.mobile-header-list{
    border-bottom: 1px solid rgba(158, 158, 158, 0.3) !important;
}

.mobile-header-list .dropdown-title{
    border-bottom: none !important;
    font-size: 16px!important; 
    padding: 0px!important; 
    padding-left: 45px!important; 
    font-weight: normal;
}

.mobile-header-list .upside::after{
    transform: rotate(180deg);
}

</style>
<!-- End Google Tag Manager -->
<!-- Global site tag (gtag.js) - Google Ads: 474915276 -->
<!-- <script async src="https://www.googletagmanager.com/gtag/js?id=AW-474915276"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-474915276');
</script> -->

</head>

<body class="post-template-default single single-post postid-139720 single-format-standard custom-background custom-background-white">

    <script>
        // Dark mode script

        const gfgThemeList = Object.freeze({
            LIGHT: "gfgThemeLight",
            DARK: "gfgThemeDark"
        })
        const getThemeFromCookie = () => {
            let gfg_def_theme = "";
            let cookies = document.cookie;
            let cooks = cookies.split(";");
        
            for (let i = 0; i < cooks.length; i++) {   
                let icook = cooks[i].split("=");
                if (icook[0].trim() == "gfg_theme") {
                    gfg_def_theme = icook[1].trim();
                }
            }
            return gfg_def_theme
        }
        if(!(post_slug.includes('premium-plans-payment/') || post_slug.includes('premium-plans/'))){
            var isDarkMode = getThemeFromCookie() == gfgThemeList.DARK ? true : false;
            document.querySelector("body").setAttribute("data-dark-mode", isDarkMode);
        }
 

        function setSearchBarFocus() {
          const myTimeout = setTimeout(searchBarFocus, 0);
          function searchBarFocus() {
            document.getElementById("gcse-search-input").focus();
          }
        }

        
    </script>

    <!-- <div class="header-main__wrapper not-fixed"> -->
    <nav>
    <div class="header-main__wrapper">

        <a class="gfg-stc" style="top:0" href="#main">Skip to content</a>

        <a href="https://www.geeksforgeeks.org/" aria-label="Logo" class="header-main__logo">
            <div class="_logo">
                <!-- Original Logo -->
                <img class="gfg_logo_img" style="height: 30px; width: 80px; max-width: fit-content;" src="https://media.geeksforgeeks.org/gfg-gg-logo.svg" alt="geeksforgeeks">
            </div>
        </a>
        <div class="header-main__container">
            <!-- for mobile only -->
            
        <!-- For Web view only -->
        <ul class="header-main__list"><li class="header-main__list-item Header_1" data-parent="false" aria-expanded="true" data-expandable="true"><span>Courses</span><i class="gfg-icon gfg-icon_arrow-down gfg-icon_header"></i><ul class="mega-dropdown Screen_1"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/dsa-to-development-coding-guide?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">DSA to Development</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/data-science-live?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">Machine Learning & Data Science</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/mastering-generative-ai-and-chat-gpt?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">Generative AI & ChatGPT</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/search?query=AWS&itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">Become AWS Certified</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>DSA Courses</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/dsa-self-paced?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">Data Structure & Algorithm(C++/JAVA)</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/Data-Structures-With-Python?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">Data Structure & Algorithm(Python)</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/data-structures-and-algorithms-in-javascript?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">Data Structure & Algorithm(JavaScript)</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Programming Languages</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/cpp-programming-basic-to-advanced?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">CPP</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/Java-Programming-basic-to-advanced?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">Java</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/Python-Foundation?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">Python</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/javascript?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">JavaScript</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses/c-Programming-basic-to-advanced?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">C</a></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/courses?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=courses" target="_self">All Courses</a></li></ul></li><li class="header-main__list-item Header_2" data-parent="false" aria-expanded="true" data-expandable="true"><span>Tutorials</span><i class="gfg-icon gfg-icon_arrow-down gfg-icon_header"></i><ul class="mega-dropdown Screen_1"><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><a href="https://www.geeksforgeeks.org/python3-tutorial/?ref=ghm" class="remove-anchor__decoration" target="_self" style="display: inline-flex; padding: 0;">Python Tutorial</a><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/taking-input-in-python/?ref=outind" target="_self">Taking Input in Python</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/python-operators/?ref=outind" target="_self">Python Operators</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/python-data-types/?ref=outind" target="_self">Python Data Types</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Python Loops and Control Flow</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/python3-if-if-else-nested-if-if-elif-statements/?ref=outind" target="_self">Python Conditional Statements</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/loops-in-python/?ref=outind" target="_self">Python Loops</a></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/python-functions/?ref=outind" target="_self">Python Functions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/python-oops-concepts/?ref=outind" target="_self">Python OOPS Concept</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/python-data-structures-and-algorithms/?ref=outind" target="_self">Python Data Structures</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/python-exception-handling/?ref=outind" target="_self">Python Exception Handling</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/file-handling-python/?ref=outind" target="_self">Python File Handling</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/python-exercises-practice-questions-and-solutions/?ref=outind" target="_self">Python Exercises</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Java</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/java/?ref=outind" target="_self">Learn Java Programming Language</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/collections-in-java-2/?ref=outind" target="_self">Java Collections</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/java-8-features/?ref=outind" target="_self">Java 8 Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/java-programming-examples/?ref=outind" target="_self">Java Programs</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Java Interview Questions</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/java-interview-questions/?ref=outind" target="_self">Java Interview Questions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/core-java-interview-questions-for-freshers/?ref=outind" target="_self">Core Java Interview Questions-Freshers</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/top-20-java-multithreading-interview-questions-answers/?ref=outind" target="_self">Java Multithreading Interview Questions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/oops-interview-questions/?ref=outind" target="_self">OOPs Interview Questions and Answers</a></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/java-exercises/?ref=outind" target="_self">Java Exercises</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Java Quiz</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/quizzes/50-java-language-mcqs-with-answers-2/?ref=outind" target="_self">Java Quiz</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/java-multiple-choice-questions/?ref=outind" target="_self">Core Java MCQ</a></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/java-projects/?ref=outind" target="_self">Java Projects</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Advance Java</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/spring/?ref=outind" target="_self">Spring Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/spring-boot/?ref=outind" target="_self">Spring Boot Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/spring-boot-interview-questions/?ref=outind" target="_self">Spring Boot Interview Questions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/spring-mvc/?ref=outind" target="_self">Spring MVC Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/spring-mvc-interview-questions/?ref=outind" target="_self">Spring MVC Interview Questions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/hibernate-tutorial/?ref=outind" target="_self">Hibernate Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/hibernate-interview-questions/?ref=outind" target="_self">Hibernate Interview Questions</a></li></ul></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Programming Languages</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/javascript/?ref=outind" target="_self">JavaScript</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/c-plus-plus/?ref=outind" target="_self">C++</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/r-tutorial/?ref=outind" target="_self">R Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/sql-tutorial/?ref=outind" target="_self">SQL</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/php-tutorial/?ref=outind" target="_self">PHP</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/csharp-programming-language/?ref=outind" target="_self">C#</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/c-programming-language/?ref=outind" target="_self">C</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/scala-programming-language/?ref=outind" target="_self">Scala</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/perl-programming-language/?ref=outind" target="_self">Perl</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/golang/?ref=outind" target="_self">Go Language</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/kotlin-programming-language/?ref=outind" target="_self">Kotlin</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><a href="https://www.geeksforgeeks.org/data-structures/?ref=ghm" class="remove-anchor__decoration" target="_self" style="display: inline-flex; padding: 0;">System Design</a><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/system-design-tutorial/?ref=ghm" target="_self">System Design Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/software-design-patterns/?ref=outind" target="_self">Software Design Patterns</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/complete-roadmap-to-learn-system-design/?ref=outind" target="_self">System Design Roadmap</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/top-10-system-design-interview-questions-and-answers/?ref=outind" target="_self">Top 10 System Design Interview Questions and Answers</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Interview Corner</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/company-preparation/?ref=outind" target="_self">Company Preparation</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/interview-preparation-for-software-developer/?ref=outind" target="_self">Top Topics</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://practice.geeksforgeeks.org/company-tags/?ref=outind" target="_self">Practice Company Questions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/company-interview-corner/?ref=outind" target="_self">Interview Experiences</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/experienced-interview-experiences-company-wise/?ref=outind" target="_self">Experienced Interviews</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/internship-interview-experiences-company-wise/?ref=outind" target="_self">Internship Interviews</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/competitive-programming-a-complete-guide/?ref=outind" target="_self">Competitive Programming</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/quiz-corner-gq/?ref=outind" target="_self">Multiple Choice Quizzes</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/aptitude-questions-and-answers/?ref=outind" target="_self">Aptitude for Placements</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Computer Science Subjects</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/operating-systems/?ref=outind" target="_self">Operating System</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/dbms/?ref=outind" target="_self">DBMS</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/computer-network-tutorials/?ref=outind" target="_self">Computer Networks</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/engineering-mathematics-tutorials/?ref=outind" target="_self">Engineering Mathematics</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/computer-organization-and-architecture-tutorials/?ref=outind" target="_self">Computer Organization and Architecture</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/theory-of-computation-automata-tutorials/?ref=outind" target="_self">Theory of Computation</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/compiler-design-tutorials/?ref=outind" target="_self">Compiler Design</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/digital-electronics-logic-design-tutorials/#blg/?ref=outind" target="_self">Digital Logic</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/software-engineering/?ref=outind" target="_self">Software Engineering</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>DevOps</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/git-tutorial/?ref=outind" target="_self">GIT</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/aws-tutorial/?ref=outind" target="_self">AWS</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/docker-tutorial/?ref=outind" target="_self">Docker</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/kubernetes-tutorial/?ref=outind" target="_self">Kubernetes</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/microsoft-azure/?ref=outind" target="_self">Microsoft Azure Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/google-cloud-platform-tutorial/?ref=outind" target="_self">Google Cloud Platform</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Linux</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/linux-tutorial/?ref=outind" target="_self">Linux Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/linux-commands/?ref=outind" target="_self">Linux Commands A-Z</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/linux-commands-cheat-sheet/?ref=outind" target="_self">Linux Commands Cheatsheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/permissions-in-linux/?ref=outind" target="_self">File Permission Commands</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/beginners-guide-to-linux-system-administration/?ref=outind" target="_self">Linux System Administration</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/linux-file-system/?ref=outind" target="_self">Linux File System</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-linux-shell-shell-scripting/?ref=outind" target="_self">Linux Shell Scripting</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/network-configuration-trouble-shooting-commands-linux/?ref=outind" target="_self">Linux Networking</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/linux-interview-questions/?ref=outind" target="_self">Linux Interview Questions</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Software Testing</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/software-testing-tutorial/?ref=outind" target="_self">Software Testing Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/software-engineering/?ref=outind" target="_self">Software Engineering Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/software-testing-interview-questions/?ref=outind" target="_self">Testing Interview Questions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/jira-tutorial/?ref=outind" target="_self">Jira</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Databases</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/dbms/?ref=outind" target="_self">DBMS Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/sql-tutorial/?ref=outind" target="_self">SQL Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/postgresql-tutorial/?ref=outind" target="_self">PostgreSQL Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/mongodb-tutorial/?ref=outind" target="_self">MongoDB Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/sql-interview-questions/?ref=outind" target="_self">SQL Interview Questions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/mysql-interview-questions/?ref=outind" target="_self">MySQL Interview Questions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/pl-sql-interview-questions/?ref=outind" target="_self">PL/SQL Interview Questions</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Android</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/android-tutorial/?ref=outind" target="_self">Android Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/android-studio-tutorial/?ref=outind" target="_self">Android Studio Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/kotlin-android-tutorial/?ref=outind" target="_self">Kotlin For Android</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/android-projects-from-basic-to-advanced-level/?ref=outind" target="_self">Android Projects</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/top-50-android-interview-questions-answers-sde-i-to-sde-iii/?ref=outind" target="_self">Android Interview Questions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/6-weeks-of-android-app-development-free-project-based-learning/?ref=outind" target="_self">6 Weeks of Android App Development</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Excel</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/excel-tutorial/?ref=outind" target="_self">MS Excel Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-ms-excel/?ref=outind" target="_self">Introduction to MS Excel</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/data-analysis-in-excel/?ref=outind" target="_self">Data Analysis in Excel</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/basic-excel-formulas-and-functions/?ref=outind" target="_self">Basic Excel Formulas & Functions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/instant-data-analysis-in-advanced-excel/?ref=outind" target="_self">Data Analysis in Advanced Excel</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/workbooks-in-microsoft-excel/?ref=outind" target="_self">Workbooks</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/statistical-functions-in-excel-with-examples/?ref=outind" target="_self">Statistical Functions</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/data-visualization-in-excel/?ref=outind" target="_self">Data Visualization in Excel</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/pivot-tables-in-excel/?ref=outind" target="_self">Pivot Tables in Excel</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/working-with-excel-spreadsheets-in-python/?ref=outind" target="_self">Excel Spreadsheets in Python</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/basic-excel-shortcuts/?ref=outind" target="_self">Basic Excel Shortcuts</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Mathematics</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/number-theory/?ref=outind" target="_self">Number System</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/algebra/?ref=outind" target="_self">Algebra</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/linear-algebra/?ref=outind" target="_self">Linear Algebra</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/math-trigonometry/?ref=outind" target="_self">Trigonometry</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/set-theory/?ref=outind" target="_self">Set Theory</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/statistics/?ref=outind" target="_self">Statistics</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/probability-in-maths/?ref=outind" target="_self">Probability</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/geometry/?ref=outind" target="_self">Geometry</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/mensuration/?ref=outind" target="_self">Mensuration</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/logarithms/?ref=outind" target="_self">Logarithms</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/math-calculus/?ref=outind" target="_self">Calculus</a></li></ul></li></ul></li><li class="header-main__list-item Header_3" data-parent="false" aria-expanded="true" data-expandable="true"><span>DSA</span><i class="gfg-icon gfg-icon_arrow-down gfg-icon_header"></i><ul class="mega-dropdown Screen_1"><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Data Structures</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/array-data-structure-guide/?ref=outind" target="_self">Arrays</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/matrix/?ref=outind" target="_self">Matrix</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/string-data-structure/?ref=outind" target="_self">Strings</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-linked-list-data-structure/?ref=ghm" target="_self">Linked List</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/stack-data-structure/?ref=outind" target="_self">Stack</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/queue-data-structure/?ref=outind" target="_self">Queue</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-tree-data-structure-and-algorithm-tutorials/?ref=outind" target="_self">Tree</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/heap-data-structure/?ref=outind" target="_self">Heap</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/hashing-data-structure/?ref=outind" target="_self">Hashing</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/?ref=outind" target="_self">Graph</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-set-data-structure-and-algorithm-tutorials/?ref=outind" target="_self">Set Data Structure</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-map-data-structure-and-algorithm-tutorials/?ref=outind" target="_self">Map Data Structure</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/advanced-data-structures/?ref=outind" target="_self">Advanced Data Structure</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-data-structures/?ref=outind" target="_self">Data Structures Tutorial</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Algorithms</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Analysis of Algorithms</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/design-and-analysis-of-algorithms/?ref=outind" target="_self">Design and Analysis of Algorithms</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/asymptotic-notation-and-analysis-based-on-input-size-of-algorithms/?ref=outind" target="_self">Asymptotic Analysis</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/types-of-asymptotic-notations-in-complexity-analysis-of-algorithms/?ref=outind" target="_self">Asymptotic Notations</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/worst-average-and-best-case-analysis-of-algorithms/?ref=outind" target="_self">Worst, Average and Best Cases</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Searching Algorithms</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/linear-search/?ref=outind" target="_self">Linear Search</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/binary-search/?ref=outind" target="_self">Binary Search</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/searching-algorithms/?ref=outind" target="_self">Searching Algorithms Tutorial</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Sorting Algorithms</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/selection-sort/?ref=outind" target="_self">Selection Sort</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/bubble-sort/?ref=outind" target="_self">Bubble Sort</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/insertion-sort/?ref=outind" target="_self">Insertion Sort</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/merge-sort/?ref=outind" target="_self">Merge Sort</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/quick-sort/?ref=outind" target="_self">Quick Sort</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/heap-sort/?ref=outind" target="_self">Heap Sort</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/counting-sort/?ref=outind" target="_self">Counting Sort</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/radix-sort/?ref=outind" target="_self">Radix Sort</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/bucket-sort-2/?ref=outind" target="_self">Bucket Sort</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-sorting-algorithm/?ref=outind" target="_self">Sorting Algorithms Tutorial</a></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-greedy-algorithm-data-structures-and-algorithm-tutorials/?ref=outind" target="_self">Greedy Algorithms</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-dynamic-programming-data-structures-and-algorithm-tutorials/?ref=outind" target="_self">Dynamic Programming</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-graphs-data-structure-and-algorithm-tutorials/?ref=outind" target="_self">Graph Algorithms</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-pattern-searching-data-structure-and-algorithm-tutorial/?ref=outind" target="_self">Pattern Searching</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-recursion-data-structure-and-algorithm-tutorials/?ref=outind" target="_self">Recursion</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-backtracking-data-structure-and-algorithm-tutorials/?ref=outind" target="_self">Backtracking</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-divide-and-conquer-algorithm-data-structure-and-algorithm-tutorials/?ref=outind" target="_self">Divide and Conquer</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/mathematical-algorithms/?ref=outind" target="_self">Mathematical Algorithms</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/geometric-algorithms/?ref=outind" target="_self">Geometric Algorithms</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-bitwise-algorithms-data-structures-and-algorithms-tutorial/?ref=outind" target="_self">Bitwise Algorithms</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/randomized-algorithms/?ref=outind" target="_self">Randomized Algorithms</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-branch-and-bound-data-structures-and-algorithms-tutorial/?ref=outind" target="_self">Branch and Bound</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-algorithms/?ref=outind" target="_self">Algorithms Tutorial</a></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/learn-data-structures-and-algorithms-dsa-tutorial/?ref=outind" target="_self">DSA Tutorial</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Practice</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&sortBy=submissions&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">All DSA Problems</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/problem-of-the-day?itm_source=geeksforgeeksitm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Problem of the Day</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Company Wise Coding Practice</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&company=Amazon&sortBy=submissions&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Amazon</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&company=Microsoft&sortBy=submissions&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Microsoft</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&company=Flipkart&sortBy=submissions&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Flipkart</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&sortBy=submissions&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Explore All</a></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&curated[]=1&sortBy=submissions&curated_names[]=SDE Sheet?itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">GfG SDE Sheet</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Practice Problems Difficulty Wise</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&difficulty=School&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">School</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&difficulty=Basic&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Basic</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&difficulty=Easy&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Easy</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&difficulty=Medium&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Medium</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&difficulty=Hard&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Hard</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Language Wise Coding Practice</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&category=CPP&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">CPP</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&category=Java&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Java</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?category=python&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Python</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Curated DSA Lists</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&sprint=ca8ae412173dbd8346c26a0295d098fd&sortBy=submissions&sprint_name=Beginner's DSA Sheet&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Beginner's DSA Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&sprint=50746f92a895c22a50504ac0c1fb9c84&sortBy=submissions&sprint_name=Top 50 Array Problems&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Top 50 Array Problems</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&sprint=57184072610b884e5df3584cc534115d&sortBy=submissions&sprint_name=Top 50 String Problems&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Top 50 String Problems</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&sprint=93d672753b74440c7427214c8ebf866d&sortBy=submissions&sprint_name=Top 50 DP Problems&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Top 50 DP Problems</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&sprint=405e9db0f353691ad3b2d546b19145e9&sortBy=submissions&sprint_name=Top 50 Graph Problems&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Top 50 Graph Problems</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/explore?page=1&sprint=5f24de84b65bf7c4f4399c8111e26b81&sortBy=submissions&sprint_name=Top 50 Tree Problems&itm_source=geeksforgeeks&itm_medium=main_header_outIndia&itm_campaign=DSA_Header" target="_self">Top 50 Tree Problems</a></li></ul></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/competitive-programming-a-complete-guide/?ref=outind" target="_self">Competitive Programming</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Company Wise SDE Sheets</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/facebookmeta-sde-sheet-interview-questions-and-answers/?ref=outind" target="_self">Facebook SDE Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/amazon-sde-sheet-interview-questions-and-answers/?ref=outind" target="_self">Amazon SDE Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/apple-sde-sheet-interview-questions-and-answers/?ref=outind" target="_self">Apple SDE Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/netflix-sde-sheet-interview-questions-and-answers/?ref=outind" target="_self">Netflix SDE Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/google-sde-sheet-interview-questions-and-answers/?ref=outind" target="_self">Google SDE Sheet</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>DSA Cheat Sheets</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/sde-sheet-a-complete-guide-for-sde-preparation/?ref=outind" target="_self">SDE Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/most-asked-dsa-interview-problems-for-beginners/?ref=outind" target="_self">DSA Sheet for Beginners</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/must-do-coding-questions-for-companies-like-amazon-microsoft-adobe/?ref=outind" target="_self">FAANG Coding Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/must-do-coding-questions-for-product-based-companies/?ref=outind" target="_self">Product-Based Coding Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/must-coding-questions-company-wise/?ref=outind" target="_self">Company-Wise Preparation Sheet</a></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/top-100-data-structure-and-algorithms-dsa-interview-questions-topic-wise/?ref=outind" target="_self">Top Interview Questions</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Puzzles</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/puzzles/?ref=outind" target="_self">All Puzzles</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/top-100-puzzles-asked-in-interviews/?ref=outind" target="_self">Top 100 Puzzles Asked In Interviews</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/top-20-puzzles-commonly-asked-during-sde-interviews/?ref=outind" target="_self">Top 20 Puzzles Commonly Asked During SDE Interviews</a></li></ul></li></ul></li><li class="header-main__list-item Header_4" data-parent="false" aria-expanded="true" data-expandable="true"><span>Data Science</span><i class="gfg-icon gfg-icon_arrow-down gfg-icon_header"></i><ul class="mega-dropdown Screen_1"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/python-programming-language/?ref=outind" target="_self">Python Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/r-tutorial/?ref=outind" target="_self">R Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/machine-learning/?ref=outind" target="_self">Machine Learning</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/data-science-with-python-tutorial/?ref=outind" target="_self">Data Science using Python</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/r-programming-for-data-science/?ref=outind" target="_self">Data Science using R</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Data Science Packages</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/pandas-tutorial/?ref=outind" target="_self">Pandas Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/numpy-tutorial/?ref=outind" target="_self">NumPy Tutorial</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Data Visualization</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/python-data-visualization-tutorial/?ref=outind" target="_self">Python Data Visualization Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/data-visualization-in-r/?ref=outind" target="_self">Data Visualization with R</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Data Analysis</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/data-analysis-with-python/?ref=outind" target="_self">Data Analysis with Python</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/data-analysis-using-r/?ref=outind" target="_self">Data Analysis with R</a></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/deep-learning-tutorial/?ref=outind" target="_self">Deep Learning</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/natural-language-processing-nlp-tutorial/?ref=outind" target="_self">NLP Tutorial</a></li></ul></li><li class="header-main__list-item Header_5" data-parent="false" aria-expanded="true" data-expandable="true"><span>Web Tech</span><i class="gfg-icon gfg-icon_arrow-down gfg-icon_header"></i><ul class="mega-dropdown Screen_1"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/html-tutorial/?ref=outind" target="_self">HTML Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/css-tutorial/?ref=outind" target="_self">CSS Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/javascript/?ref=outind" target="_self">JavaScript Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/php-tutorial/?ref=outind" target="_self">PHP Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/react-tutorial/?ref=outind" target="_self">ReactJS Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/nodejs/?ref=outind" target="_self">NodeJS Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/bootstrap/?ref=outind" target="_self">Bootstrap Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/typescript/?ref=outind" target="_self">Typescript</a></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Web Development Using Python</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Django</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/django-tutorial/?ref=outind" target="_self">Django Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/top-django-projects-for-beginners/?ref=outind" target="_self">Django Projects</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/django-interview-questions/?ref=outind" target="_self">Django Interview Questions</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Flask</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_3"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/flask-tutorial/?ref=outind" target="_self">Flask Tutorial</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/flask-projects/?ref=outind" target="_self">Flask Projects</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/flask-interview-questions-and-answers/?ref=outind" target="_self">Flask Interview Questions</a></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/postman-tutorial/?ref=outind" target="_self">Postman</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/introduction-to-github/?ref=outind" target="_self">Github</a></li></ul></li><li class="mega-dropdown__list-item" data-parent="false" aria-expanded="true" data-expandable="true"><span>Cheat Sheets</span><i class="gfg-icon gfg-icon_arrow-right"></i><ul class="mega-dropdown Screen_2"><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/html-cheat-sheet-a-basic-guide-to-html/?ref=outind" target="_self">HTML Cheat Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/css-cheat-sheet-a-basic-guide-to-css/?ref=outind" target="_self">CSS Cheat Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/javascript-cheat-sheet-a-basic-guide-to-javascript/?ref=outind" target="_self">JavaScript Cheat Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/react-cheat-sheet/?ref=outind" target="_self">React Cheat Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/angular-cheat-sheet-a-basic-guide-to-angular/?ref=outind" target="_self">Angular Cheat Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/jquery-cheat-sheet-a-basic-guide-to-jquery/?ref=outind" target="_self">jQuery Cheat Sheet</a></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/bootstrap-cheatsheet-a-basic-guide-to-bootstrap/?ref=outind" target="_self">Bootstrap Cheat Sheet</a></li></ul></li><li class="mega-dropdown__list-item" data-child="true" aria-expanded="false" data-expandable="false"><a href="https://www.geeksforgeeks.org/web-development/?ref=outind" target="_self">Learn Complete Web Development</a></li></ul></li></ul>
        <!-- right now only search is visible for mobile view because of css and all are visible for web view -->
            <ul class="header-main__left-list" data-nl="false">
                <li class="header-main__left-list-item gcse-search_li p-relative" aria-expanded="false" data-expandable="false">
                    <div class="gcse-form-search-suggestion_wrapper">
                        <form id="gcse-form" class="gcse-form_class p-relative closeChatScreen" data-sm="false">
                            <span class="front-search-icon"><i class="gfg-icon gfg-icon_search gfg-icon_white gcse-search__icon gcse-search-icon_grey"></i> </span>
                            <input class="gcse-search-input__wrapper" id="gcse-search-input" aria-expanded="false" placeholder="Search..." autocomplete="off" />
                            <i class="gfg-icon gfg-icon_times gfg-icon_white hide-search"></i>
                            <button  aria-label="search" type="submit" class="gcse-search__btn not-expanded">
                                <i class="gfg-icon gfg-icon_search gfg-icon_white gcse-search__icon"></i>
                            </button>
                        </form>
                        <div class="gfg-search-suggestion_wrapper" style="display:none"></div>
                    <div>
                </li>
                                <li>
                    <div class="darkMode-wrap" data-mode="Switch to Dark Mode">
                        <button aria-label="toggle theme" data-gfg-action="toggleGFGTheme">
                            <div id="darkMode-wrap-red-dot" style="height:12px;width:12px;background-color:#EB2222;border-radius:999999px;position:absolute;top:4px;right:0;display:none;"></div>
                            <i class="gfg-icon gfg-icon_dark-mode"></i>
                        </button>
                        <span id="darkModeTooltipText"></span>
                    </div>
                </li>
                                
                <li class="header-main__left-list-item google-translate-parent-element" aria-expanded="false" data-expanded="true">
                    <div class="translate" id="g_translater">
                        <div id="google_translate_element" data-show="false"></div>
                    </div>
                    <i class ="gfg-icon gfg-icon_translate googleTranslateToggle" data-gfg-action="google_translate_element"></i>
                    <!-- removed below code from here to load google translate js dynamically -->
                    <!-- <script>
                        var m = false;
                        function googleTranslateElementInit() {
                            new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
                            setTimeout(function(){
                                if (jQuery( window ).width() < 768){
                                    m = true;
                                     jQuery('#g_translater').detach().appendTo('#google_translate_mobile');                            
                                }
                            }, 7000);
                        }
                        jQuery( window ).resize(function() {
                            if (jQuery( window ).width() < 768 && m == false){
                                m = true;
                                jQuery('#g_translater').detach().appendTo('#google_translate_mobile');  
                            } else if (jQuery( window ).width() >= 768 && m == true){
                                m = false;
                                jQuery('#g_translater').detach().prependTo('.google-translate-parent-element');                            
                            }
                        });
                    </script> -->
                </li>
                <li id="userProfileId" class="header-main__left-list-item p-relative" aria-expanded="false" data-expandable="false">
                    <!-- Profile Section to be added via JS -->
                </li>
                            </ul>
        </div>

        <!-- for mobile only -->
        
        <!-- for mobile only -->
               
       </div>
    </nav>
    <div class="header-main__slider">
        <button aria-label="sub header slider previous" class="header-main__slider-arrow previous hideIt">
            <i class="gfg-icon gfg-icon_arrow-left gicon-centered"></i>
        </button>
        <!-- main content for leftbar -->
        <ul id="hslider">
        <li><a href="https://www.geeksforgeeks.org/arrays-in-java/?ref=shm">Java Arrays</a></li><li><a href="https://www.geeksforgeeks.org/strings-in-java/?ref=shm">Java Strings</a></li><li><a href="https://www.geeksforgeeks.org/object-oriented-programming-oops-concept-in-java/?ref=shm">Java OOPs</a></li><li><a href="https://www.geeksforgeeks.org/java-collection-tutorial/?ref=shm">Java Collection</a></li><li><a href="https://www.geeksforgeeks.org/java-8/?ref=shm">Java 8 Tutorial</a></li><li><a href="https://www.geeksforgeeks.org/java-multithreading-tutorial/?ref=shm">Java Multithreading</a></li><li><a href="https://www.geeksforgeeks.org/exceptions-in-java/?ref=shm">Java Exception Handling</a></li><li><a href="https://www.geeksforgeeks.org/java-programming-examples/?ref=shm">Java Programs</a></li><li><a href="https://www.geeksforgeeks.org/top-50-java-project-ideas-for-beginners-advanced/?ref=shm">Java Project</a></li><li><a href="https://www.geeksforgeeks.org/java-collections-interview-questions/?ref=shm">Java Collections Interview</a></li><li><a href="https://www.geeksforgeeks.org/interview-questions-for-java-professionals/?ref=shm">Java Interview Questions</a></li><li><a href="https://www.geeksforgeeks.org/quizzes/50-java-language-mcqs-with-answers-2/?ref=shm">Java MCQs</a></li><li><a href="https://www.geeksforgeeks.org/spring/?ref=shm">Spring</a></li><li><a href="https://www.geeksforgeeks.org/spring-mvc/?ref=shm">Spring MVC</a></li><li><a href="https://www.geeksforgeeks.org/spring-boot/?ref=shm">Spring Boot</a></li><li><a href="https://www.geeksforgeeks.org/hibernate-tutorial/?ref=shm">Hibernate</a></li>        </ul>
        <button aria-label="sub header slider next" class="header-main__slider-arrow next hideIt">
            <i class="gfg-icon gfg-icon_arrow-right gicon-centered"></i>
        </button>
    </div>
    <button id="scrollTopBtn" title="Scroll to Top" type="button" class="btn btn-success">&#x25B2;</button>
    <!-- .top-spacing to give space on single pages-->
    <div id="main" class="wrapper single-page">

<script>
    if(post_slug.includes('premium-plans-payment/') || post_slug.includes('premium-plans/')){
        $(".header-main__slider").remove();
    }
    //getting tags for the page type data
    let mobileView = false;
    let pageTags = JSON.parse('null');
    let allTags = JSON.parse('["Java","ProgrammingLanguage"]');
</script>

<script>
    window.have_dsa_term = false;
    // var practiceTab = ; 
</script>

<style>
    .wrapper {
        flex-direction: column !important;
    }
    /* spinner css */
    @keyframes spinner {
        to {transform: rotate(360deg);}
    }
    
    .spinner:before {
        content: '';
        box-sizing: border-box;
        position: absolute;
        top: 50%;
        left: 50%;
        width: 20px;
        height: 20px;
        margin-top: -10px;
        margin-left: -10px;
        border-radius: 50%;
        border: 2px solid #ccc;
        border-top-color: #000;
        animation: spinner .6s linear infinite;
    }

    .report-loader{
        position: relative;
        
    }

    .report-loader.spinner{
        margin-left: 16px;
    }
    .badges{
        display: flex;
        align-items: center;
        position: relative;
    }
    .badges .gfg-badge-icon.md::after{
        transform: scale(0.25);
        position:relative;
        top: 2px;
        left: -2px;
    }
    .sep{
        margin: 0px 5px;
        font-size: 20px;
        color: var(--badge-name-color);
    }
    .pub-count{
        font-size: 14px;
        font-family: var(--font-secondary);
    }
    .badge-details{
        display:none;
    }
    .badges{
        cursor: pointer;
        position: relative;
        /* width: 0px;
        height: 20px;
        top: -32px; */
    }
    .badge-icon{
        display: flex;
        align-items: center;
    }
    .badge-content{
        margin-left: 9px;
    }
    .badge-name{
        color: var(--badge-nam-color);
        font-weight: 600;
        font-size: 16px;
        text-transform: capitalize;
    }
    .badge-data{
        color: #A5A4A4;
        font-size: 10px;
    }
    .badges:hover .badge-details{
        display: block;
        background: var(--badge-bg);
        padding: 10px 18px 10px 18px;
        position: absolute;
        width: 175px;
        top: -10px;
        z-index: 10;
        left: 112%;
        box-shadow: rgb(100 100 111 / 20%) 0px 7px 29px 0px;
        border-radius: 5px;
        /* transform-origin: top right; */
    }
    .badge-details::before {
        content: "";
        position: absolute;
        transform: rotate(90deg);
        /* transform-origin: right; */
        left: -6px;
        top: 50%;
        margin-left: -17px;
        border-width: 12px;
        border-style: solid;
        border-color: var(--badge-bg) transparent transparent transparent;
        margin-top: -12px;
    }
    .badge-icon .icon{
        border: 1px solid var(--icon-border-color);
        padding: 4px 3px;
        border-radius: 4px;
        width: 22px;
        height: 24px;
        position: relative;
    }
    .b-icon-pos{
        position: relative;
        top: -34px;
        left: -34px;
    }
    /* article viewer */
    .article--viewer .a-wrapper{
        margin-top: 0px !important;
    }
    .content{
        padding-top: 10px !important;
    }
    .u-name{
        font-size: 14px;
    }
    .article--viewer_content .a-wrapper .content{
        padding-bottom: 10px !important;
    }
    .likeTooltipBottom{
        font-size: 14px;
    }
    @media (max-width: 434px) {
        .article-buttons.show-bg{
            margin-top: 56px !important;
        }
    }
    @media (max-width: 730px),
            ((min-width: 992px) and (max-width:1100px))  {
        .article--viewer .media{
            position: relative;
        }
        .article--viewer .media{
            margin-bottom: 0px !important;
        }
        .badges:hover .badge-details{
            top: -56px;
            left: 62px;
        }
        .badge-details::before{
            transform: rotate(0deg);
            left: 10%;
            top: 117%;
        }
        .article-buttons.show-bg{
            margin-top: 22px;
            top: 0px !important;
        }
    }
    @media ((min-width:731px) and (max-width:1223px)) {
        .article-buttons.show-bg{
            top: 18px;
        }
    }
    @media ((min-width:993px) and (max-width:1190px)) {
        .article--viewer .media{
            position: relative;
        }
        .article--viewer .media{
            margin-bottom: 25px !important;
        }
    }
</style>
<!-- Survey modal implementation -->
<script>
    function getCookie(name) {
        function escape(s) { return s.replace(/([.*+?\^$(){}|\[\]\/\\])/g, '\\$1'); }
        var match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape(name) + '=([^;]*)'));
        return match ? match[1] : null;
    }
</script>
<!-- END Survey modal implementation-->

<!-- Open in App Button and CSS-->

<!-- Above code is for old openInApp pop-up with open in app and continue buttons-->

<div id='openInApp-modal' class='openInApp'>
    <a href = 'https://geeksforgeeksapp.page.link/?link=https://www.geeksforgeeks.org/output-java-program-set-7/?type%3Darticle%26id%3D139720&apn=free.programming.programming&isi=1641848816&ibi=org.geeksforgeeks.GeeksforGeeksDev&efr=1' class='openInAppLink'>
        <span style='color: #fff;'>Open In App</span>
    </a>
</div>
    <script>
        var consentValue = localStorage.getItem("gfg_cc");
        var isIOS = !!navigator.platform && /iPad|iPhone|iPod|MacIntel/.test(navigator.platform) && navigator.maxTouchPoints > 0;
        const isSafari = navigator.userAgent.indexOf("Safari") > -1;
        const isMozilla = navigator.userAgent.indexOf("Mozilla") > -1;
        if(consentValue){
            if(window.innerHeight > window.innerWidth && navigator.maxTouchPoints > 1 && (isSafari || isMozilla || navigator.userAgentData.mobile)){
                $('.openInApp').css({
                    display: "block"
                });
                $('#scrollTopBtn').css({
                    bottom: "44px"
                });
                //adding a new class to check stats for clicks on iOS and Android
                isIOS ? jQuery('.openInAppLink').addClass("oia-iOS") : $('.openInAppLink').addClass("oia-android");      //for openInApp Link
            }
        }
        
    </script>
    <style>
        .openInApp{
            display: none;
            bottom: 0px;
            width: 100%;
            position: fixed;
            z-index: 1025;
            opacity: 0.93;
        }
        .openInAppLink{
            height: 44px;
            background: var(--color-gfg);
            font-weight: bold;
            display: block;
            text-align: center;
            padding: 12px;
            font-size: large;
        }
        .openInAppLink, .openInAppLink:hover, .openInAppLink:active, .openInAppLink:visited, .openInAppLink:focus {
            text-decoration:none;
        }
    </style>
<!-- END Open in App Button and CSS-->
<div class="container-fluid bg-light" id="home-page" style="position: relative; max-width:100%;">
    <div class="article-page_flex">
            <div class="sidebar_wrapper  auto_leftbar ">
          <div class="sideBar autoLeftBar_oin_non_sticky" style="height: unset !important">
                <!-- <div class="sideBar--wrap newLeftbar oinLeftbar autoLeftBar_oin_child"> -->
                <div class="sideBar--wrap newLeftbar autoLeftBar_oin_child">
                                        <div id="GFG_AD_Leftsidebar_300x250_chained_1"></div>
                        <div id="GFG_AD_Leftsidebar_300x250_chained_2"></div>
                        <div id="GFG_AD_Leftsidebar_300x250_chained_3"></div>
                        <div id="GFG_AD_Leftsidebar_300x600_chained_1"></div>
                    </div>
                               </div>
             <div id="GFG_AD_Desktop_LeftSideBar_Docked_160x600" style="max-width:160px; max-height:600px"></div>
        </div>
                <div class="leftBar">
            <div class="article--viewer">
                <div class="article--viewer_content">
                    <div class="a-wrapper">
                        <div class="" style="z-index:9999 !important;position:relative;">
                        </div>
                        <article class="content post-139720 post type-post status-publish format-standard hentry category-java" id="post-139720">
                                                                                   <!-- when comment system will be scalable from practice side then we will display  Article/Discussion tab-->
                            <div class="main_wrapper" style="display:flex;">
                                                                <div style="width: 100%;">
                                        <div class="article-title">
                                            <h1>Output of Java Program | Set 7</h1>
                                        </div>
                                                                                    <div class="last_updated_parent">
                                                <div>
                                                    <span class="strong">Last Updated : </span>
                                                    <span>28 Jun, 2021</span>
                                                </div>

                                                 <!-- three dot menu -->
                                                <div class="three_dot_dropdown"> 
                                                                                                            <div style="display: flex;">
                                                                                                                    <div pid="139720" ptitle="Output of Java Program | Set 7" class="top-summary-icon-div ">
                                                                <div class="three_dot_dropdown_div tooltip">
                                                                    <span class="summary_tooltiptext">Summarize</span>
                                                                    <div class="summarize_header">
                                                                    <i class= "summary_button" style="position: relative;"></i>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                                                                                                                                                        <div pid="139720" ptitle="Output of Java Program | Set 7" class="article--viewer_comment tooltip top-comment-icon-div">
                                                                    <span class="comment_tooltiptext">Comments</span>
                                                                    <div class="three_dot_dropdown_div" data-gfg-action='loadComments'>
                                                                        <div class="comment_header">
                                                                        <i class= "discussion_button" style="position: relative; transform: scale(0.9);"></i>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                                                                        <div pid="139720" ptitle="Output of Java Program | Set 7" class="article--viewer_improve tooltip">
                                                                <span class="improve_tooltiptext">Improve</span>
                                                                <div class="three_dot_dropdown_div three_dot_dropdown_improve" onclick="improveArticleCall()">
                                                                    <div class="improve_wrapper_top">
                                                                    <i class="gfg-icon gfg-icon-pencil  gfg-icon_edit" style="position: relative; z-index: 3;"></i>
                                                                    </div>
                                                                </div>
                                                                <!-- <button onclick="improveArticleCall()">
                                                                    <i class="gfg-icon gfg-icon_edit"></i>
                                                                </button> -->
                                                            </div> 
                                                                                                                    <!-- three dots -->
                                                        <ul class="dropbtn icons btn-right showLeft" onclick="showDropdown()">
                                                            <li>
                                                                                                                            </li>
                                                            <li></li>
                                                            <li></li>
                                                        </ul>
                                                    </div>
                                                </div> 
                                            </div>
                                                                            </div>
                                                            </div>
                            <!-- menu -->
                            <div id="myDropdown" class="three_dot_dropdown_content">
                                        <div class="article-buttons drop" onmouseleave="closeKebabMenu()">
                                            <!-- If the status of the summary API is true than we are showing the summarize button otherwise not  -->
                                                                                         <div pid="139720" ptitle="Output of Java Program | Set 7" class="improve_article--viewer tooltip">
                                                <div class="three_dot_dropdown_div three_dot_dropdown_improve" onclick="suggestionArticleCall()" style="margin-top: 1px;">
                                                    <div class="three_dot_dropdown_inner_div improve_dot_dropdown_inner_div">
                                                        <i class="gfg-icon gfg-icon_suggest_changes gfg-icon_edit"></i>
                                                        <span>Suggest changes</span>
                                                    </div>
                                                </div>
                                            </div>                                                                                          <div pid="139720" class="article--viewer_like tooltip">
                                            <div class="three_dot_dropdown_div three_dot_dropdown_likearticle" onmouseleave='toggleLikeElementVisibility("showLikesContainer", false)'  onmouseenter='toggleLikeElementVisibility("showLikesContainer", true)'>
                                                    <div class="showLikesContainer"> 
                                                        <span class="likeTooltip">Like Article</span>
                                                    </div>
                                                    <div class="three_dot_dropdown_inner_div" data-gfg-action="like-article" data-bookmark-value="0">
                                                        <i class="gfg-icon gfg-icon_thumbs"></i>
                                                        <span>Like</span>
                                                    </div>
                                                </div>
<!-- <button data-gfg-action="like-article" data-bookmark-value="0">
                                                    <i class="gfg-icon gfg-icon_thumbs"></i>
                                                </button> -->
                                            </div>
                                            <div pid="139720" class="article--viewer_bookmark tooltip">
                                                <div class="three_dot_dropdown_div three_dot_dropdown_save">
                                                    <div class="three_dot_dropdown_inner_div" data-gfg-action="bookmark-article" data-bookmark-value="0">
                                                        <i class="gfg-icon gfg-icon_bookmark"></i>
                                                        <span>Save</span>
                                                    </div>
                                                </div>
<!-- <button data-gfg-action="bookmark-article" data-bookmark-value="0">
                                                    <i class="gfg-icon gfg-icon_bookmark"></i>
                                                </button> -->
                                            </div>
                                            <div pid="139720" class="article--viewer_share tooltip">
                                                <div class="three_dot_dropdown_div three_dot_dropdown_share" onmouseleave="closeShareModal()" onmouseenter="openShareModal()">
                                                    <div style="display: flex;align-items: center;" class="three_dot_dropdown_inner_div" data-gfg-action="share-article" data-bookmark-value="0">
                                                        <i class="gfg-share-icon"></i>
                                                        <span>Share</span>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="article--viewer_report tooltip">
                                                <div class="three_dot_dropdown_div three_dot_dropdown_reportarticle">
                                                    <div class="three_dot_dropdown_inner_div" data-gfg-action="report-article" onclick="report_article();">
                                                        <i class="gfg-icon gfg-icon_report"></i>
                                                        <span>Report</span>
                                                    </div>
                                                </div>
<!-- <button data-gfg-action="like-article" data-bookmark-value="0">
                                                    <i class="gfg-icon gfg-icon_thumbs"></i>
                                                </button> -->
                                            </div>
                                            <div class="article--viewer_Gnews tooltip">
                                                <a class="three_dot_dropdown_inner_div Gnews_wrapper" href ='https://news.google.com/publications/CAAqBwgKMLTrzwsw44bnAw?hl=en-IN&gl=IN&ceid=IN%3Aen' target="_blank">
                                                    <img class="gfg-icon_Gnews no-zoom-in-cursor" src=https://media.geeksforgeeks.org/auth-dashboard-uploads/Google-news.svg  loading="lazy" alt="News"></img>
                                                    <span class='kebab_menu_news_text'>Follow</span>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                            <div class="text">
                                                                <p><strong>Difficulty level : </strong> Intermediate</p>
<p>Predict the output of following Java Programs.</p>
<p><strong>Program 1 :</strong></p>
<div class="code-block">
<div class="code-gutter">
<div class="editor-buttons-container">
<div class="editor-buttons">
<div class="editor-buttons-div" title="Run and Edit">
                                    <i id="copy-code-button" title="Copy Code" class="gfg-icon gfg-icon_copy code-sidebar-button padding-2px copy-code-button"></i></p>
<div  id = "run-and-edit-loader" class="ring-load"></div>
<p>                                    <i id="run-and-edit-button" title="Edit Code" lang="java"  class="gfg-icon gfg-icon_edit_1 padding-2px code-sidebar-button"></i><br />
                                    <i id="close-code-editor-button" title="Close Editor" class="gfg-icon gfg-icon_close-editor padding-2px code-sidebar-button close-code-editor-button"></i></p>
<div id = "run-code-loader" class="ring-load"></div>
<p>                                    <i id="run-code-button" lang="java" title="Run Code and See Output" class="gfg-icon gfg-icon_play padding-2px code-sidebar-button"></i></p>
<div  id = "generate-url-loader" class="ring-load"></div>
<p>                                    <i id="generate-url-and-run-button" title="Run Code and Generate IDE URL" lang="java"  class="gfg-icon gfg-icon_link padding-2px code-sidebar-button generate-url-and-run-button"></i><br />
                                    <i title="Dark Mode" class="gfg-icon gfg-icon_dark-toggle padding-2px code-sidebar-button dark-editor-button"></i><br />
                                    <i id = "edit-on-ide-button" title="Edit on IDE"  lang="java" class="gfg-icon gfg-icon_code padding-2px code-sidebar-button edit-on-ide-button"></i>
                                </div>
</p></div>
</p></div>
</p></div>
<div class= "code-container">
<div id="highlighter_957163" class="syntaxhighlighter nogutter  ">
<table border="0" cellpadding="0" cellspacing="0">
<tbody>
<tr>
<td class="code">
<div class="container">
<div class="line number1 index0 alt2"><code class="keyword">public</code> <code class="keyword">class</code> <code class="plain">Calculator </code></div>
<div class="line number2 index1 alt1"><code class="plain">{ </code></div>
<div class="line number3 index2 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">int</code> <code class="plain">num = </code><code class="value">100</code><code class="plain">; </code></div>
<div class="line number4 index3 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code> <code class="keyword">void</code> <code class="plain">calc(</code><code class="keyword">int</code> <code class="plain">num)&nbsp; { </code><code class="keyword">this</code><code class="plain">.num = num * </code><code class="value">10</code><code class="plain">;&nbsp; } </code></div>
<div class="line number5 index4 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code> <code class="keyword">void</code> <code class="plain">printNum()&nbsp;&nbsp;&nbsp;&nbsp; { System.out.println(num); } </code></div>
<div class="line number6 index5 alt1"><code class="undefined spaces">&nbsp;</code>&nbsp;</div>
<div class="line number7 index6 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code> <code class="keyword">static</code> <code class="keyword">void</code> <code class="plain">main(String[] args) </code></div>
<div class="line number8 index7 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">{ </code></div>
<div class="line number9 index8 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">Calculator obj = </code><code class="keyword">new</code> <code class="plain">Calculator(); </code></div>
<div class="line number10 index9 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">obj.calc(</code><code class="value">2</code><code class="plain">); </code></div>
<div class="line number11 index10 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">obj.printNum(); </code></div>
<div class="line number12 index11 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">} </code></div>
<div class="line number13 index12 alt2"><code class="plain">} </code></div>
</div>
</td>
</tr>
</tbody>
</table>
</div></div>
<div class="code-editor-container"></div>
</p></div>
<div class="code-output-container">
<div class = "output-block">
                        <i id="output-icon" title="Output" class="gfg-icon gfg-icon_arrow-right-editor padding-2px code-sidebar-button output-icon"></i></p>
<pre class="output-pre"></pre>
</p></div>
<div class = "ide-link-div">
                        <i id="copy-url-button" title="Copy Generated Ide URL" class="gfg-icon gfg-icon_copy padding-2px code-sidebar-button copy-url-button"></i></p>
<pre id="ide-url"></pre>
</p></div>
</p></div>
<p><strong>Options :</strong><br />
A) 20<br />
B) 100<br />
C) 1000<br />
D) 2<br />
<strong>Answer : A) 20 </strong><br />
<strong>Explanation :</strong> Here the class instance variable name(num) is same as <em>calc()</em> method local variable name(num). So for referencing class instance variable from  <em>calc()</em> method, <strong><a href="https://www.geeksforgeeks.org/this-reference-in-java/">this</a></strong> keyword is used. So in statement <strong>this.num = num * 10</strong>, <em>num</em> represents local variable of the method whose value is 2 and <em>this.num</em> represents class instance variable whose initial value is 100. Now in <em>printNum()</em> method, as it has no local variable whose name is same as class instance variable, so we can directly use <em>num</em> to reference instance variable, although <em>this.num</em> can be used.</p>
<p>&nbsp;</p>
<p><strong>Program 2 :</strong></p>
<div class="code-block">
<div class="code-gutter">
<div class="editor-buttons-container">
<div class="editor-buttons">
<div class="editor-buttons-div" title="Run and Edit">
                                    <i id="copy-code-button" title="Copy Code" class="gfg-icon gfg-icon_copy code-sidebar-button padding-2px copy-code-button"></i></p>
<div  id = "run-and-edit-loader" class="ring-load"></div>
<p>                                    <i id="run-and-edit-button" title="Edit Code" lang="java"  class="gfg-icon gfg-icon_edit_1 padding-2px code-sidebar-button"></i><br />
                                    <i id="close-code-editor-button" title="Close Editor" class="gfg-icon gfg-icon_close-editor padding-2px code-sidebar-button close-code-editor-button"></i></p>
<div id = "run-code-loader" class="ring-load"></div>
<p>                                    <i id="run-code-button" lang="java" title="Run Code and See Output" class="gfg-icon gfg-icon_play padding-2px code-sidebar-button"></i></p>
<div  id = "generate-url-loader" class="ring-load"></div>
<p>                                    <i id="generate-url-and-run-button" title="Run Code and Generate IDE URL" lang="java"  class="gfg-icon gfg-icon_link padding-2px code-sidebar-button generate-url-and-run-button"></i><br />
                                    <i title="Dark Mode" class="gfg-icon gfg-icon_dark-toggle padding-2px code-sidebar-button dark-editor-button"></i><br />
                                    <i id = "edit-on-ide-button" title="Edit on IDE"  lang="java" class="gfg-icon gfg-icon_code padding-2px code-sidebar-button edit-on-ide-button"></i>
                                </div>
</p></div>
</p></div>
</p></div>
<div class= "code-container">
<div id="highlighter_37046" class="syntaxhighlighter nogutter  ">
<table border="0" cellpadding="0" cellspacing="0">
<tbody>
<tr>
<td class="code">
<div class="container">
<div class="line number1 index0 alt2"><code class="keyword">public</code> <code class="keyword">class</code> <code class="plain">MyStuff </code></div>
<div class="line number2 index1 alt1"><code class="plain">{ </code></div>
<div class="line number3 index2 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">String name; </code></div>
<div class="line number4 index3 alt1"><code class="undefined spaces">&nbsp;</code>&nbsp;</div>
<div class="line number5 index4 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">MyStuff(String n) {&nbsp; name = n;&nbsp; } </code></div>
<div class="line number6 index5 alt1"><code class="undefined spaces">&nbsp;</code>&nbsp;</div>
<div class="line number7 index6 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code> <code class="keyword">static</code> <code class="keyword">void</code> <code class="plain">main(String[] args) </code></div>
<div class="line number8 index7 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">{ </code></div>
<div class="line number9 index8 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">MyStuff m1 = </code><code class="keyword">new</code> <code class="plain">MyStuff(</code><code class="string">"guitar"</code><code class="plain">); </code></div>
<div class="line number10 index9 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">MyStuff m2 = </code><code class="keyword">new</code> <code class="plain">MyStuff(</code><code class="string">"tv"</code><code class="plain">); </code></div>
<div class="line number11 index10 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">System.out.println(m2.equals(m1)); </code></div>
<div class="line number12 index11 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">} </code></div>
<div class="line number13 index12 alt2"><code class="undefined spaces">&nbsp;</code>&nbsp;</div>
<div class="line number14 index13 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="color1">@Override</code></div>
<div class="line number15 index14 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code> <code class="keyword">boolean</code> <code class="plain">equals(Object obj) </code></div>
<div class="line number16 index15 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">{ </code></div>
<div class="line number17 index16 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">MyStuff m = (MyStuff) obj; </code></div>
<div class="line number18 index17 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">if</code> <code class="plain">(m.name != </code><code class="keyword">null</code><code class="plain">)&nbsp; { </code><code class="keyword">return</code> <code class="keyword">true</code><code class="plain">;&nbsp; } </code></div>
<div class="line number19 index18 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">return</code> <code class="keyword">false</code><code class="plain">; </code></div>
<div class="line number20 index19 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">} </code></div>
<div class="line number21 index20 alt2"><code class="plain">} </code></div>
</div>
</td>
</tr>
</tbody>
</table>
</div></div>
<div class="code-editor-container"></div>
</p></div>
<div class="code-output-container">
<div class = "output-block">
                        <i id="output-icon" title="Output" class="gfg-icon gfg-icon_arrow-right-editor padding-2px code-sidebar-button output-icon"></i></p>
<pre class="output-pre"></pre>
</p></div>
<div class = "ide-link-div">
                        <i id="copy-url-button" title="Copy Generated Ide URL" class="gfg-icon gfg-icon_copy padding-2px code-sidebar-button copy-url-button"></i></p>
<pre id="ide-url"></pre>
</p></div>
</p></div>
<p><strong>Options :</strong><br />
A) The output is true and MyStuff fulfills the Object.equals() contract.<br />
B) The output is false and MyStuff fulfills the Object.equals() contract.<br />
C) The output is true and MyStuff does NOT fulfill the Object.equals() contract.<br />
D) The output is false and MyStuff does NOT fulfill the Object.equals() contract.     </p>
<p><strong>Answer :</strong> C) The output is true and MyStuff does NOT fulfill the Object.equals() contract.<br />
<strong>Explanation :</strong> As <em>equals(Object obj)</em> method in Object class, compares two objects on the basis of equivalence relation. But here we are just confirming that the object is null or not, So it doesn&#8217;t fulfill <a href="https://www.geeksforgeeks.org/overriding-equals-method-in-java/">Object.equals()</a> contract. As <em>m1</em> is not null, true will be printed.</p>
<p>&nbsp;</p>
<p><strong>Program 3 :</strong></p>
<div class="code-block">
<div class="code-gutter">
<div class="editor-buttons-container">
<div class="editor-buttons">
<div class="editor-buttons-div" title="Run and Edit">
                                    <i id="copy-code-button" title="Copy Code" class="gfg-icon gfg-icon_copy code-sidebar-button padding-2px copy-code-button"></i></p>
<div  id = "run-and-edit-loader" class="ring-load"></div>
<p>                                    <i id="run-and-edit-button" title="Edit Code" lang="java"  class="gfg-icon gfg-icon_edit_1 padding-2px code-sidebar-button"></i><br />
                                    <i id="close-code-editor-button" title="Close Editor" class="gfg-icon gfg-icon_close-editor padding-2px code-sidebar-button close-code-editor-button"></i></p>
<div id = "run-code-loader" class="ring-load"></div>
<p>                                    <i id="run-code-button" lang="java" title="Run Code and See Output" class="gfg-icon gfg-icon_play padding-2px code-sidebar-button"></i></p>
<div  id = "generate-url-loader" class="ring-load"></div>
<p>                                    <i id="generate-url-and-run-button" title="Run Code and Generate IDE URL" lang="java"  class="gfg-icon gfg-icon_link padding-2px code-sidebar-button generate-url-and-run-button"></i><br />
                                    <i title="Dark Mode" class="gfg-icon gfg-icon_dark-toggle padding-2px code-sidebar-button dark-editor-button"></i><br />
                                    <i id = "edit-on-ide-button" title="Edit on IDE"  lang="java" class="gfg-icon gfg-icon_code padding-2px code-sidebar-button edit-on-ide-button"></i>
                                </div>
</p></div>
</p></div>
</p></div>
<div class= "code-container">
<div id="highlighter_863862" class="syntaxhighlighter nogutter  ">
<table border="0" cellpadding="0" cellspacing="0">
<tbody>
<tr>
<td class="code">
<div class="container">
<div class="line number1 index0 alt2"><code class="keyword">class</code> <code class="plain">Alpha </code></div>
<div class="line number2 index1 alt1"><code class="plain">{ </code></div>
<div class="line number3 index2 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code> <code class="plain">String type = </code><code class="string">"a "</code><code class="plain">; </code></div>
<div class="line number4 index3 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code> <code class="plain">Alpha() {&nbsp; System.out.print(</code><code class="string">"alpha "</code><code class="plain">); } </code></div>
<div class="line number5 index4 alt2"><code class="plain">} </code></div>
<div class="line number6 index5 alt1"><code class="undefined spaces">&nbsp;</code>&nbsp;</div>
<div class="line number7 index6 alt2"><code class="keyword">public</code> <code class="keyword">class</code> <code class="plain">Beta </code><code class="keyword">extends</code> <code class="plain">Alpha </code></div>
<div class="line number8 index7 alt1"><code class="plain">{ </code></div>
<div class="line number9 index8 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code> <code class="plain">Beta()&nbsp; {&nbsp; System.out.print(</code><code class="string">"beta "</code><code class="plain">);&nbsp; } </code></div>
<div class="line number10 index9 alt1"><code class="undefined spaces">&nbsp;</code>&nbsp;</div>
<div class="line number11 index10 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">void</code> <code class="plain">go() </code></div>
<div class="line number12 index11 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">{ </code></div>
<div class="line number13 index12 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">type = </code><code class="string">"b "</code><code class="plain">; </code></div>
<div class="line number14 index13 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">System.out.print(</code><code class="keyword">this</code><code class="plain">.type + </code><code class="keyword">super</code><code class="plain">.type); </code></div>
<div class="line number15 index14 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">} </code></div>
<div class="line number16 index15 alt1"><code class="undefined spaces">&nbsp;</code>&nbsp;</div>
<div class="line number17 index16 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code> <code class="keyword">static</code> <code class="keyword">void</code> <code class="plain">main(String[] args) </code></div>
<div class="line number18 index17 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">{ </code></div>
<div class="line number19 index18 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">new</code> <code class="plain">Beta().go(); </code></div>
<div class="line number20 index19 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">} </code></div>
<div class="line number21 index20 alt2"><code class="plain">} </code></div>
</div>
</td>
</tr>
</tbody>
</table>
</div></div>
<div class="code-editor-container"></div>
</p></div>
<div class="code-output-container">
<div class = "output-block">
                        <i id="output-icon" title="Output" class="gfg-icon gfg-icon_arrow-right-editor padding-2px code-sidebar-button output-icon"></i></p>
<pre class="output-pre"></pre>
</p></div>
<div class = "ide-link-div">
                        <i id="copy-url-button" title="Copy Generated Ide URL" class="gfg-icon gfg-icon_copy padding-2px code-sidebar-button copy-url-button"></i></p>
<pre id="ide-url"></pre>
</p></div>
</p></div>
<p><strong>Options :</strong><br />
A) alpha beta b b<br />
B) alpha beta a b<br />
C) beta alpha b b<br />
D) beta alpha a b</p>
<p><strong>Answer :</strong> A) alpha beta b b<br />
<strong>Explanation :</strong> The statement <strong>new Beta().go() </strong>executes in two phases. In first phase <em>Beta</em> class constructor is called. There is no instance member present in <em>Beta</em> class. So now <em>Beta</em> class constructor is executed. As <em>Beta</em> class extends  <em>Alpha</em> class, so call goes to <em>Alpha</em> class constructor as first statement by default(Put by the compiler) is <strong>super()</strong> in the <em>Beta</em> class constructor. Now as one instance variable(<em>type</em>) is present in <em>Alpha</em> class, so it will get memory and now <em>Alpha</em> class constructor is executed, then call return to <em>Beta</em> class constructor next statement. So <em>alpha beta</em> is printed.<br />
In second phase <em>go()</em> method is called on this object. As there is only one variable(<em>type</em>) in the object whose value is <em>a</em>. So it will be changed to <em>b</em> and printed two times. The  <a href="https://www.geeksforgeeks.org/super-keyword/">super keyword</a> here is of no use. </p>
<p>&nbsp;</p>
<p><strong>Program 4 :</strong></p>
<div class="code-block">
<div class="code-gutter">
<div class="editor-buttons-container">
<div class="editor-buttons">
<div class="editor-buttons-div" title="Run and Edit">
                                    <i id="copy-code-button" title="Copy Code" class="gfg-icon gfg-icon_copy code-sidebar-button padding-2px copy-code-button"></i></p>
<div  id = "run-and-edit-loader" class="ring-load"></div>
<p>                                    <i id="run-and-edit-button" title="Edit Code" lang="java"  class="gfg-icon gfg-icon_edit_1 padding-2px code-sidebar-button"></i><br />
                                    <i id="close-code-editor-button" title="Close Editor" class="gfg-icon gfg-icon_close-editor padding-2px code-sidebar-button close-code-editor-button"></i></p>
<div id = "run-code-loader" class="ring-load"></div>
<p>                                    <i id="run-code-button" lang="java" title="Run Code and See Output" class="gfg-icon gfg-icon_play padding-2px code-sidebar-button"></i></p>
<div  id = "generate-url-loader" class="ring-load"></div>
<p>                                    <i id="generate-url-and-run-button" title="Run Code and Generate IDE URL" lang="java"  class="gfg-icon gfg-icon_link padding-2px code-sidebar-button generate-url-and-run-button"></i><br />
                                    <i title="Dark Mode" class="gfg-icon gfg-icon_dark-toggle padding-2px code-sidebar-button dark-editor-button"></i><br />
                                    <i id = "edit-on-ide-button" title="Edit on IDE"  lang="java" class="gfg-icon gfg-icon_code padding-2px code-sidebar-button edit-on-ide-button"></i>
                                </div>
</p></div>
</p></div>
</p></div>
<div class= "code-container">
<div id="highlighter_319550" class="syntaxhighlighter nogutter  ">
<table border="0" cellpadding="0" cellspacing="0">
<tbody>
<tr>
<td class="code">
<div class="container">
<div class="line number1 index0 alt2"><code class="keyword">public</code> <code class="keyword">class</code> <code class="plain">Test </code></div>
<div class="line number2 index1 alt1"><code class="plain">{ </code></div>
<div class="line number3 index2 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code> <code class="keyword">static</code> <code class="keyword">void</code> <code class="plain">main(String[] args) </code></div>
<div class="line number4 index3 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">{ </code></div>
<div class="line number5 index4 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">StringBuilder s1 = </code><code class="keyword">new</code> <code class="plain">StringBuilder(</code><code class="string">"Java"</code><code class="plain">); </code></div>
<div class="line number6 index5 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">String s2 = </code><code class="string">"Love"</code><code class="plain">; </code></div>
<div class="line number7 index6 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">s1.append(s2); </code></div>
<div class="line number8 index7 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">s1.substring(</code><code class="value">4</code><code class="plain">); </code></div>
<div class="line number9 index8 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">int</code> <code class="plain">foundAt = s1.indexOf(s2); </code></div>
<div class="line number10 index9 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">System.out.println(foundAt); </code></div>
<div class="line number11 index10 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">} </code></div>
<div class="line number12 index11 alt1"><code class="plain">} </code></div>
</div>
</td>
</tr>
</tbody>
</table>
</div></div>
<div class="code-editor-container"></div>
</p></div>
<div class="code-output-container">
<div class = "output-block">
                        <i id="output-icon" title="Output" class="gfg-icon gfg-icon_arrow-right-editor padding-2px code-sidebar-button output-icon"></i></p>
<pre class="output-pre"></pre>
</p></div>
<div class = "ide-link-div">
                        <i id="copy-url-button" title="Copy Generated Ide URL" class="gfg-icon gfg-icon_copy padding-2px code-sidebar-button copy-url-button"></i></p>
<pre id="ide-url"></pre>
</p></div>
</p></div>
<p><strong>Options :</strong><br />
A) -1<br />
B) 3<br />
C) 4<br />
D) A <strong>StringIndexOutOfBoundsException</strong> is thrown at runtime.<br />
<strong>Answer :</strong> C) 4<br />
<strong>Explanation :</strong> <em>append(String str)</em> method,concatenate the str to <em>s1</em>. The <em>substring(int index)</em> method return the String from the given index to the end. But as there is no any String variable to store the returned string,so it will be destroyed.Now <em>indexOf(String s2)</em> method return the index of first occurrence of <em>s2</em>. So 4 is printed as s1=&#8221;JavaLove&#8221;.</p>
<p>&nbsp;</p>
<p><strong>Program 5 :</strong></p>
<div class="code-block">
<div class="code-gutter">
<div class="editor-buttons-container">
<div class="editor-buttons">
<div class="editor-buttons-div" title="Run and Edit">
                                    <i id="copy-code-button" title="Copy Code" class="gfg-icon gfg-icon_copy code-sidebar-button padding-2px copy-code-button"></i></p>
<div  id = "run-and-edit-loader" class="ring-load"></div>
<p>                                    <i id="run-and-edit-button" title="Edit Code" lang="java"  class="gfg-icon gfg-icon_edit_1 padding-2px code-sidebar-button"></i><br />
                                    <i id="close-code-editor-button" title="Close Editor" class="gfg-icon gfg-icon_close-editor padding-2px code-sidebar-button close-code-editor-button"></i></p>
<div id = "run-code-loader" class="ring-load"></div>
<p>                                    <i id="run-code-button" lang="java" title="Run Code and See Output" class="gfg-icon gfg-icon_play padding-2px code-sidebar-button"></i></p>
<div  id = "generate-url-loader" class="ring-load"></div>
<p>                                    <i id="generate-url-and-run-button" title="Run Code and Generate IDE URL" lang="java"  class="gfg-icon gfg-icon_link padding-2px code-sidebar-button generate-url-and-run-button"></i><br />
                                    <i title="Dark Mode" class="gfg-icon gfg-icon_dark-toggle padding-2px code-sidebar-button dark-editor-button"></i><br />
                                    <i id = "edit-on-ide-button" title="Edit on IDE"  lang="java" class="gfg-icon gfg-icon_code padding-2px code-sidebar-button edit-on-ide-button"></i>
                                </div>
</p></div>
</p></div>
</p></div>
<div class= "code-container">
<div id="highlighter_205208" class="syntaxhighlighter nogutter  ">
<table border="0" cellpadding="0" cellspacing="0">
<tbody>
<tr>
<td class="code">
<div class="container">
<div class="line number1 index0 alt2"><code class="keyword">class</code> <code class="plain">Writer </code></div>
<div class="line number2 index1 alt1"><code class="plain">{ </code></div>
<div class="line number3 index2 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code>&nbsp; <code class="keyword">static</code> <code class="keyword">void</code> <code class="plain">write() </code></div>
<div class="line number4 index3 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">{ </code></div>
<div class="line number5 index4 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">System.out.println(</code><code class="string">"Writing..."</code><code class="plain">); </code></div>
<div class="line number6 index5 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">} </code></div>
<div class="line number7 index6 alt2"><code class="plain">} </code></div>
<div class="line number8 index7 alt1"><code class="keyword">class</code> <code class="plain">Author </code><code class="keyword">extends</code> <code class="plain">Writer </code></div>
<div class="line number9 index8 alt2"><code class="plain">{ </code></div>
<div class="line number10 index9 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code>&nbsp; <code class="keyword">static</code> <code class="keyword">void</code> <code class="plain">write() </code></div>
<div class="line number11 index10 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">{ </code></div>
<div class="line number12 index11 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">System.out.println(</code><code class="string">"Writing book"</code><code class="plain">); </code></div>
<div class="line number13 index12 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">} </code></div>
<div class="line number14 index13 alt1"><code class="plain">} </code></div>
<div class="line number15 index14 alt2"><code class="undefined spaces">&nbsp;</code>&nbsp;</div>
<div class="line number16 index15 alt1"><code class="keyword">public</code> <code class="keyword">class</code> <code class="plain">Programmer </code><code class="keyword">extends</code> <code class="plain">Author </code></div>
<div class="line number17 index16 alt2"><code class="plain">{ </code></div>
<div class="line number18 index17 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code>&nbsp; <code class="keyword">static</code> <code class="keyword">void</code> <code class="plain">write() </code></div>
<div class="line number19 index18 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">{ </code></div>
<div class="line number20 index19 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">System.out.println(</code><code class="string">"Writing code"</code><code class="plain">); </code></div>
<div class="line number21 index20 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">} </code></div>
<div class="line number22 index21 alt1"><code class="undefined spaces">&nbsp;</code>&nbsp;</div>
<div class="line number23 index22 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="keyword">public</code> <code class="keyword">static</code> <code class="keyword">void</code> <code class="plain">main(String[] args) </code></div>
<div class="line number24 index23 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">{ </code></div>
<div class="line number25 index24 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">Author a = </code><code class="keyword">new</code> <code class="plain">Programmer(); </code></div>
<div class="line number26 index25 alt1"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">a.write(); </code></div>
<div class="line number27 index26 alt2"><code class="undefined spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="plain">} </code></div>
<div class="line number28 index27 alt1"><code class="plain">} </code></div>
</div>
</td>
</tr>
</tbody>
</table>
</div></div>
<div class="code-editor-container"></div>
</p></div>
<div class="code-output-container">
<div class = "output-block">
                        <i id="output-icon" title="Output" class="gfg-icon gfg-icon_arrow-right-editor padding-2px code-sidebar-button output-icon"></i></p>
<pre class="output-pre"></pre>
</p></div>
<div class = "ide-link-div">
                        <i id="copy-url-button" title="Copy Generated Ide URL" class="gfg-icon gfg-icon_copy padding-2px code-sidebar-button copy-url-button"></i></p>
<pre id="ide-url"></pre>
</p></div>
</p></div>
<p><strong>Options :</strong><br />
A) Writing&#8230;<br />
B) Writing book<br />
C) Writing code<br />
D) Compilation fails</p>
<p><strong>Answer :</strong> B) Writing book<br />
<strong>Explanation :</strong> Since static methods can&#8217;t be overridden, it doesn&#8217;t matter which class object is created. As <em>a</em> is a<em> Author</em> referenced type, so always <em>Author</em> class method is called. If we remove <em>write()</em> method from <em>Author </em>class then <em>Writer </em> class method is called, as <em>Author </em>class extends <em>Writer</em> class.</p>
<div hideAd="MID"></div><br/><div id="AP_G4GR_6"></div>

                                    <div class='article_bottom_text'></div><br>
                                                                          <div id="video-tab-content" class="video-tab-content">
                                        <div style="text-align: center; margin: 20px 0px;" id="GFG_AD_InContent_Desktop_728x280"></div>
                                                                              </div>
                                                                <div class="d-row content-bw article-pgnavi v-divider-gfg"style="margin-top: 20px;">
                            <div class="article-pgnavi_prev"><div class="comment_div" data-title="Comments"><button class="author_footer_btn"  data-gfg-action="loadComments">
    <div class='discussion_panel'>
        <i class='discussion_button'>
        </i>
        Comment
    </div></button></div><div class="trigger-div"><button class="author_footer_btn"><div class="more_info">More info<span class="more_info_uparrow gfg-icon gfg-icon_arrow-down-thin"></span></div></button></div></div>
                                                              <div class="article-pgnavi_next">
                                    <a href="https://www.geeksforgeeks.org/data-types-in-java/?ref=next_article" class="pg-head">
                                        <span>Next Article</span>
                                        <span class="gfg-icon gfg-icon_next"></span>
                                    </a>
                                    <!-- <div class="pg-meta">8 Min Read&ensp;|&ensp;<a href="#">Java</a></div> -->
                                    <div class="pg-main">
                                        <a href="https://www.geeksforgeeks.org/data-types-in-java/?ref=next_article">Java Data Types</a>
                                    </div>
                                </div>
                                                        </div>
                            <div class="article-meta-author-details hidden-div">
                                        <div class="article-meta-author-details-block">
                                            <div class="article-meta-author-details-profile-display">
                                                <div class="author_info">
                                                <div class="article-meta-author-details-profile-display-icon">
                                                    <div class="image-wrap auth-external-author" style="position: relative; pointer-events: none; user-select: none;"><p class="profileCard-profile-picture" style="background-color:#E5F9DB;margin: 0px;">G</p></div>                                                </div>
                                                <div class="article-meta-author-details-profile-display-name" >
                                                    <div class="info" style="position: unset;">
<div class="name" style="cursor: default;">
    <span class="footer_author_name" style="font-weight: 600">Gaurav Miglani</span>
</div>
</div>                                                </div>
                                                </div>
                                                                                            </div>
                                            
                                        </div>
                                        <div class="article_bottom_suggestion_wrapper">
                                            <div class="article_bottom_suggestion" data-title="Follow">
                                                <a href='https://news.google.com/publications/CAAqBwgKMLTrzwsw44bnAw?hl=en-IN&gl=IN&ceid=IN%3Aen' target="_blank">
                                                    <img class="gfg-icon_Gnews no-zoom-in-cursor" src=https://media.geeksforgeeks.org/auth-dashboard-uploads/Google-news.svg  loading="lazy" alt="News"></img>
                                                </a>
                                            </div> 
                                            <div pid="139720" class="article--viewer_like tooltip tooltipBottom" data-title="Like Article">
                                                <!-- <span class="tooltiptext likeTooltipBottom">Like Article</span> -->
                                                <button id="likeButton" aria-label="like article" data-gfg-action="like-article" data-bookmark-value="0" data-liked="false" style="color: #5B5A5A !important; display: flex; align-items: center; background-color: unset; margin: 0px !important; padding: 5px 0px;">
                                                    <i class="author-badge-like-button"></i>
                                                    <figure id="likeCount" style="margin-left: 3px; margin-top: 4px; color: var(--like-count-color); font-size: 14px; font-weight: 600;" class="favoriteText"></figure>
                                                </button>
                                            </div>
                                            <div class="article_bottom_suggestion" onclick="improveArticleCall()" data-title="Improve">
                                            <span class="improveTooltipBottom">Improve</span>
                                                <i class="author-badge-improvement-button"></i>
                                            </div>
                                        </div>
                                    </div>
                        </div>
                                                </article>
                        
                                                 <div class="article--recommended article--recommended_wrapper" id="similar-reads">
                                <h3 class="new-top-bar top-bar-title">Similar Reads</h3>
                                <div class="gfg-similar-reads-list">
                                    <ul class="similarReadLeftBarList"><div class='second'><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/output-java-program-set-17/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Output of Java program | Set 17
                    </div>
                    <div class="gfg-similar-read-item-subheading">1) What is the output of following program? public class Test { private static float temp() { public static float sum = 21; return(--(sum)); } public static void main(String[] args) { Test test = new Test(); System.out.println(test.temp()); } } a) 21 b) 20 c) Compilation error d) Runtime error Ans.</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">2 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/output-of-java-program-set-1/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Output of Java Program | Set 1
                    </div>
                    <div class="gfg-similar-read-item-subheading">Difficulty Level: Rookie Predict the output of the following Java Programs.Program 1: Java Code // filename Main.java class Test { protected int x, y; } class Main { public static void main(String args[]) { Test t = new Test(); System.out.println(t.x + &amp;quot; &amp;quot; + t.y); } } Output: 0 0 I</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">3 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/output-of-java-program-set-3/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Output of Java Program | Set 3
                    </div>
                    <div class="gfg-similar-read-item-subheading">Predict the output of the following Java Programs: Example1: Java Code // filename: Test.java class Test { // Declaring and initializing integer variable int x = 10; // Main driver method public static void main(String[] args) { // Creating an object of class inside main() Test t = new Test(); // Pr</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">3 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/output-java-program-set-6/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Output of Java Program | Set 6
                    </div>
                    <div class="gfg-similar-read-item-subheading">Difficulty level : Intermediate Predict the output of following Java Programs. Program 1: class First { public First() { System.out.println(&quot;a&quot;); } } class Second extends First { public Second() { System.out.println(&quot;b&quot;); } } class Third extends Second { public Third() { System.o</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">2 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/output-java-program-set-19/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Output of Java Program | Set 19
                    </div>
                    <div class="gfg-similar-read-item-subheading">Predict the output of following Java Programs. Program 1 : public class RuntimePolymorphism { public static void main(String[] args) { A a = new B(); B b = new B(); System.out.println(a.c + &quot; &quot; + a.getValue() + &quot; &quot; + b.getValue() + &quot; &quot; + b.getSuperValue()); } } class A</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">3 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/output-java-program-set-23-inheritance/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Output of Java program | Set 23 (Inheritance)
                    </div>
                    <div class="gfg-similar-read-item-subheading">Prerequisite: Inheritance in Java 1) What is the output of the following program? Java Code public class A extends B { public static String sing() { return &quot;fa&quot;; } public static void main(String[] args) { A a = new A(); B b = new A(); System.out.println(a.sing() + &quot; &quot; + b.sing())</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">3 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/output-of-java-programs-set-13-collections/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Output of Java programs | Set 13 (Collections)
                    </div>
                    <div class="gfg-similar-read-item-subheading">Prerequisite - Collections in Java 1) What is the output of the following program? Java Code import java.util.*; public class priorityQueue { public static void main(String[] args) { PriorityQueue&lt;Integer&gt; queue = new PriorityQueue&lt;&gt;(); queue.add(11); queue.add(10); queue.add(22); queue.</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">3 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/output-java-programs-set-14-constructors/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Output of Java Programs | Set 14 (Constructors)
                    </div>
                    <div class="gfg-similar-read-item-subheading">Prerequisite - Java Constructors 1) What is the output of the following program? [GFGTABS] Java class Helper { private int data; private Helper() { data = 5; } } public class Test { public static void main(String[] args) { Helper help = new Helper(); System.out.println(help.data); } } [/GFGTABS]a) C</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">3 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/output-java-programs-set-24-final-modifier/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Output of Java programs | Set 24 (Final Modifier)
                    </div>
                    <div class="gfg-similar-read-item-subheading">Difficulty level : Easy Prerequisite : final keyword in java Predict the output of following Java Programs: What will be output of following program? class Test { final int MAXIMUM; final double PI; public Test(int max) { MAXIMUM = max; } public Test(double pi) { PI = pi; } public static void main(S</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">3 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/output-java-program-set-12exception-handling/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Output of Java program | Set 12(Exception Handling)
                    </div>
                    <div class="gfg-similar-read-item-subheading">Prerequisites : Exception handling , control flow in try-catch-finally 1) What is the output of the following program? public class Test { public static void main(String[] args) { try { System.out.printf(&quot;1&quot;); int sum = 9 / 0; System.out.printf(&quot;2&quot;); } catch(ArithmeticException e</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">3 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/how-to-run-java-program/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">How to Run Java Program?
                    </div>
                    <div class="gfg-similar-read-item-subheading">Java is a popular, high-level, object-oriented programming language that was developed by James Gosling and his team at Sun Microsystems (now owned by Oracle Corporation) in the mid-1990s. It is widely used for developing various kinds of software, including web applications, desktop applications, m</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">2 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/shift-operator-in-java/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Shift Operator in Java
                    </div>
                    <div class="gfg-similar-read-item-subheading">Operators in Java are used to performing operations on variables and values. Examples of operators: +, -, *, /, &gt;&gt;, &lt;&lt;. Types of operators: Arithmetic Operator,Shift Operator,Relational Operator,Bitwise Operator,Logical Operator,Ternary Operator andAssignment Operator. In this article, w</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">4 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/system-out-println-in-java/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">System.out.println in Java
                    </div>
                    <div class="gfg-similar-read-item-subheading">Java System.out.println() is used to print an argument that is passed to it. Parts of System.out.println()The statement can be broken into 3 parts which can be understood separately: System: It is a final class defined in the java.lang package.out: This is an instance of PrintStream type, which is a</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">5 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/few-tricky-programs-in-java/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Few Tricky Programs in Java
                    </div>
                    <div class="gfg-similar-read-item-subheading">Comments that execute : Till now, we were always taught "Comments do not Execute". Let us see today "The comments that execute" Following is the code snippet: public class Testing { public static void main(String[] args) { // the line below this gives an output // \u000d System.out.println(&quot;com</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">2 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/update-the-list-items-in-java/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Java Program to Update the List Items
                    </div>
                    <div class="gfg-similar-read-item-subheading">In Java, Lists are dynamic collections that allow modifications, such as updating elements. We can use the set method to update the elements in the List. This method replaces the element at the given index with a new value, allowing modification of list contents. In this article, we will learn to up</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">2 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/java-tricky-output-questions/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Java Tricky Output Questions
                    </div>
                    <div class="gfg-similar-read-item-subheading">Question 1: What will be the Output of the below code: public class A { public static void main(String[] args) { if (true) break; } } Choices: a) Nothing b) Error Answer: b) Error Reason: Break statement can only be used with loop or switch. So, using break with if statement causes "break outside sw</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">3 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/java-hello-world-program/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Java Hello World Program
                    </div>
                    <div class="gfg-similar-read-item-subheading">Java is one of the most popular and widely used programming languages and platforms. Java is fast, reliable, and secure. Java is used in every nook and corner from desktop to web applications, scientific supercomputers to gaming consoles, cell phones to the Internet. In this article, we will learn h</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">5 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/redirecting-system-out-println-output-to-a-file-in-java/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Redirecting System.out.println() Output to a File in Java
                    </div>
                    <div class="gfg-similar-read-item-subheading">System.out.println() is used mostly to print messages to the console. However very few of us are actually aware of its working mechanism. We can use System.out.println() to print messages to other sources too, not just restricting it to the console. However, before doing so, we must reassign the sta</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">2 min read</span>
                </div>
                </a></li><li class="similarReadDropdownItem"><a href="https://www.geeksforgeeks.org/formatted-output-in-java/?ref=ml_lbp"><div class="gfg-similar-read-item-content">
                    <div class="gfg-similar-read-item-heading">Formatted Output in Java using printf()
                    </div>
                    <div class="gfg-similar-read-item-subheading">Sometimes in programming, it is essential to print the output in a given specified format. Most users are familiar with the printf function in C. Let us discuss how we can Formatting Output with printf() in Java in this article. Formatting Using Java Printf()printf() uses format specifiers for forma</div>
                </div>
                <div class="reading-time">
                    <i class="reading-time-icon" data-gfg-action="readingtime"></i>
                    <span style="color: var(--recommendation-card-text-color);font-size: 14px;font-weight: 500;line-height: 17px;">5 min read</span>
                </div>
                </a></li></div></ul>                                </div>
                            </div>
                        

                        <div class="bottom-wrap" style="padding: 0px 20px;margin-bottom: 10px;">
                                                            <div class="improved">
                                    <div class="t-head">Article Tags : </div>
                                    <ul>
                                        
            <li style="border-radius: 25px;" class="">
                <a href="https://www.geeksforgeeks.org/category/programming-language/java/?ref=article_category">Java</a>
            </li>                                    </ul>
                                                                    </div>
                                                                                        <div class="improved">
                                    <div class="t-head">Practice Tags : </div>
                                    <ul class="practice-tags">
                                        <li><a href="https://www.geeksforgeeks.org/explore?category=Java&ref=article_practice_tag">Java</a></li>                                    </ul>
                                                                    </div>
                                                    </div>
                                                <div class="vote-wrap">
                                <div style="display:none;align-items:center;justify-content:center;width:100%;">
                                    <button aria-label="like" data-type="like" class="vote-this" style="margin-right: 0; margin-left:0 ;">
                                        <i class="gfg-icon gfg-icon_like favoriteIcon"></i>
                                        <span class="favoriteLike">Like</span>
                                        <figure class="favoriteText"></figure>
                                    </button>
                                                                    </div>
                            </div>

                        </div>
                            <div class="article-meta">
                                                                                    <div class="bottom-wrap">
                              <div id="GFG_AD_InContent_Desktop_BTF_650x250" style="text-align:center;max-height: 300px;"></div>
                            </div>
                                                        <!-- end -->
                        </div>
                    </div>
                </div>
            </div>
                <div id="report_modal_content" class="report_modal_content" style="display:hidden;"></div>
        <div class="onopen-discussion-panel">
            <div class="discussion-tab">
                <div class="discussion_heading">
                    <div></div>
                    <i class="gfg-icon close-tab-icon"></i>
                </div> 
                <div class="discussion_content">                            <div style="height:100%">
                                <div style="height:100%" id="comment-system"></div>
                            </div>

                            
</div>
            </div>
        </div>  

        <div class="rightBar" style="padding-right: 5px;">
                
<style>
	.article--container_content{
		align-items: unset !important;
	}
	.sideBar {
		position: sticky !important;
	}
	.gfg-icon_switch::after {
		background-position: -40px -281px !important;
	}
	.gfg-icon_transaction::after {
		background-position: -40px -321px !important;
	}
	.header-main__profile.selected+.mega-dropdown{
		width: 225px !important;
	}
	#courses-container .course-price{
		display:none;
	}
	/* .side--container_wscard .card-content .content .meta:empty, .practiceBannerFromPlugin{
		display:none !important;
	} */
	.side--container_wscard .card-content .content .meta{
		display:block !important;
	}
	.side--container_wscard .card-content .content .meta p{
		background-color: rgba(254, 212, 91, 0.6);
		font-size: 10pt;
		font-weight: bold;
		display: inline-block;
		color: var(--color-black);
		margin-top: 15px;
		padding: 0px 5px;
	}
	#try-it{
		display:initial !important;
	}
	#try-it .try-it-div{
		line-height: 34px;
	}
	.gfg-icon_dark-mode::after {
		background-position: -40px -680px;
	}
	.side--container_wscard .head{
		font-size: 14px !important;
	}
	.nineDot-menu, .gfg-icon_ndot{
		display: none;
	}
	#text-15{
		flex-direction: column;
	}
	.mtq_correct_marker, .mtq_wrong_marker{
		display: none;
	}
	.sidebar_wrapper > :last-child{
		margin: unset !important;
		margin-left: 5px !important;
		margin-top: 20px !important;
		top: 70px !important;
	}
	.darkMode-wrap{
		bottom:1% !important;
	}
	#secondary .textwidget{
		margin-left: auto;
		margin-right: 0;
		text-align: right;
	}
	#secondary .widget_text:last-child{
		top: 70px !important;
	}
	@media(max-width:768px){
		#scrollTopBtn{
			display:none !important;
		}
	}
	.rightbar_loggedin_promo_cta{
		display:flex;
		cursor:pointer;
		margin-bottom:20px;
	}
</style>

<div id="secondary" class="widget-area">
	<div class='OINTechPromoRightBarBanner' id='rightBarSaleBanner' style='text-align:right; margin-bottom:5px;'><a href=https://www.geeksforgeeks.org/geeksforgeeks-premium-subscription?itm_source=geeksforgeeks&itm_medium=rightbar_oin&itm_campaign=premium><img src=https://media.geeksforgeeks.org/auth-dashboard-uploads/premium_oin_rbar_min.png alt='three90RightbarBannerImg' style='width:300px; height:250px;'></a></div>
	<!------------------------ text-15 (for Ads) ------------------------ -->
	<aside id="text-15" class="widget widget_text">
		<div class="textwidget">
					<div id="_GFG_ABP_Desktop_RightSideBar_ATF_300x600_2"></div>
			<div id="GFG_AD_Desktop_RightSideBar_ATF_300x250_2" style="min-width: 300px;margin-bottom:10px;"></div>
			<div id='GFG_AD_Desktop_RightSideBar_ATF_300x600' style='min-width: 300px; min-height: 600px;margin-bottom:10px;'></div>
					</div>
	</aside>

	<!------------------------ text-16 (For Ads)------------------------ -->
	<aside id="text-16" class="widget widget_text">
		<div class="textwidget">
					<div id="_GFG_ABP_Desktop_RightSideBar_MTF_300x600"></div>
			<div id='GFG_AD_Desktop_RightSideBar_MTF_300x250' style='min-width: 300px;'></div>
			<div id="_GFG_ABP_Desktop_RightSideBar_BTF_300x600"></div>
			<div id="_GFG_ABP_Desktop_RightSideBar_BTF_300x600_3"></div>
				</div>
	</aside>

	<!-- ---------------------- courses section ------------------------- -->
	<style>.right-bar-explore-more{ visibility: hidden; min-height: 230px;text-align:left;min-width:300px;max-width:300px; padding-left: 19px; padding-right: 25px; margin-top: 20px;}
        .right-bar-explore-more .title{text-align:left;font-size:20px; font-weight: 600; line-height: 22px; color:var(--em-heading);padding:14px 0;font-family:var(--font-primary)}
        .right-bar-explore-more .rightbar-sticky-ul {list-style: disc outside; padding-left: 17px;} 
        .right-bar-explore-more li{font-size: 14px !important;font-weight: 400;line-height: 18px !important;color: var(--em-text);margin: 14px 0;font-family:var(--font-primary);}
        .right-bar-explore-more li::marker{color: var(--em-text) !important;}
        .right-bar-explore-more .rightbar-sticky-ul a{text-align:left !important; color: var(--em-text); display: block !important;}  
        .right-bar-explore-more .rightbar-sticky-ul a:hover{text-decoration:underline;color:var(--em-link)!important;}
        .right-bar-explore-more hr {margin: 0;background-color: var(--tn-hr);}
        @media (max-width: 991px){
          .right-bar-explore-more{
            width: 85%;
            margin: auto;
            margin-top: 20px;
            max-width: unset;
            display: none !important;
          }
        
          #text-18 .textwidget{
            width: 100%;
          }
        }</style>    <script>
        var rightBarExploreMoreList = `<li style="color:var(--color-black)"><a href="https://www.geeksforgeeks.org/java-interview-questions/?ref=rightbar_explore" target="_blank" style="font-family:var(--font-primary)">Java Interview Questions and Answers</a></li><li style="color:var(--color-black)"><a href="https://www.geeksforgeeks.org/java/?ref=rightbar_explore" target="_blank" style="font-family:var(--font-primary)">Java Tutorial</a></li><li style="color:var(--color-black)"><a href="https://www.geeksforgeeks.org/object-oriented-programming-oops-concept-in-java/?ref=rightbar_explore" target="_blank" style="font-family:var(--font-primary)">Object Oriented Programming (OOPs) Concept in Java</a></li><li style="color:var(--color-black)"><a href="https://www.geeksforgeeks.org/arrays-in-java/?ref=rightbar_explore" target="_blank" style="font-family:var(--font-primary)">Arrays in Java</a></li><li style="color:var(--color-black)"><a href="https://www.geeksforgeeks.org/inheritance-in-java/?ref=rightbar_explore" target="_blank" style="font-family:var(--font-primary)">Inheritance in Java</a></li>`
	</script>

	<!-------------------------------- Text-18 (explore more section + ads) --------------------------->
	<aside id="text-18" class="widget widget_text">
		<div class="textwidget">
					<div class="right-bar-explore-more" style="display:none;visibility: unset;">
				<div class="title">Explore More</div>
				<ul class="rightbar-sticky-ul"></ul>
			</div>
							<div id='GFG_AD_Desktop_RightSideBar_BTF_Sticky_300x250' style='min-width: 300px;margin-bottom:10px'></div>
			<div id='GFG_AD_Desktop_RightSideBar_Docked_160x600' style='min-width: 160px;'></div><div id='GFG_AD_Desktop_RightSideBar_BTFdocked_300x600' style='min-width: 300px;'></div>
			</aside>

	<!-------------------------- Text -20 (For maintaining some CSS) ---------------------- -->
	<aside id="text-20" class="widget widget_text">
		<div class="textwidget">
		 <!-- Please do not delete this div -->
		</div>
	</aside>
</div>

                <div id="user-personal-note" style="display: none;"></div>
        </div>
    </div>
    <section class="disqus-section">
        <div class="article-page_flex">
            <div class="leftBar">
            </div>
        </div>
    </section>
</div>

<div id="video-popup" style="display:none"></div>

<link rel="stylesheet" href='https://www.geeksforgeeks.org/wp-content/themes/iconic-one/css/articleList.min.css?ver=1.7'>

<script>
$(document).ready(function() {
    var isfollowingApiCall = false;
    if ($('.follow-btn').length) {
        var articleRecommendedTop = $(".article--recommended").offset().top;
        var articleRecommendedBottom = articleRecommendedTop + $(".article--recommended").outerHeight();
        $(window).scroll(function() {
            var top_of_element = $(".article--recommended").offset().top;
            var bottom_of_element = $(".article--recommended").offset().top + $(".article--recommended").outerHeight();
            var bottom_of_screen = $(window).scrollTop() + $(window).innerHeight();
            var top_of_screen = $(window).scrollTop();
            if ((bottom_of_screen > top_of_element && top_of_screen < bottom_of_element) || 
                (bottom_of_screen > articleRecommendedTop && top_of_screen < articleRecommendedBottom) ||
                (top_of_screen > articleRecommendedBottom)) {
                if (!isfollowingApiCall) {
                    isfollowingApiCall = true;
                    setTimeout(function(){
                        if (loginData && loginData.isLoggedIn) {
                            if (loginData.userName !== $('#followAuthor').val()) {
                                is_following();
                            } else {
                                $('.profileCard-profile-picture').css('background-color', '#E7E7E7');
                            }
                        } else {
                            $('.follow-btn').removeClass('hideIt');
                        }
                    }, 3000);
                }
            }
        });
    }
    
    $(".accordion-header").click(function() {
        var arrowIcon = $(this).find('.bottom-arrow-icon');
        arrowIcon.toggleClass('rotate180');
    });

});

window.isReportArticle = false;
function report_article(){
    if (!loginData || !loginData.isLoggedIn) {
        const loginModalButton = $('.login-modal-btn')
            if (loginModalButton.length) {
                loginModalButton.click();
            }
    return;
}

    if(!window.isReportArticle){
            //to add loader
            $('.report-loader').addClass('spinner');
            jQuery('#report_modal_content').load(gfgSiteUrl+'wp-content/themes/iconic-one/report-modal.php', {
                PRACTICE_API_URL: practiceAPIURL,
                PRACTICE_URL:practiceURL
            },function(responseTxt, statusTxt, xhr){
                if(statusTxt == "error"){
                    alert("Error: " + xhr.status + ": " + xhr.statusText);
                }
            });
    }else{
        window.scrollTo({ top: 0, behavior: 'smooth' });
        $("#report_modal_content").show();
    }
} 

function closeShareModal() {
    const shareOption = document.querySelector('[data-gfg-action="share-article"]');
    shareOption.classList.remove("hover_share_menu");
    let shareModal = document.querySelector(".hover__share-modal-container");
    shareModal && shareModal.remove();
}

function openShareModal() {
    closeShareModal(); // Remove existing modal if any

    let shareModal = document.querySelector(".three_dot_dropdown_share");
    shareModal.appendChild(Object.assign(document.createElement("div"), { className: "hover__share-modal-container" }));

    document.querySelector(".hover__share-modal-container").append(
        Object.assign(document.createElement('div'), { className: "share__modal" }),
    );

    document.querySelector(".share__modal").append(Object.assign(document.createElement('h1'), { className: "share__modal-heading" }, { textContent: "Share to" }));
    const socialOptions = ["LinkedIn", "WhatsApp", "Copy Link"];

    socialOptions.forEach((socialOption) => {
        const socialContainer = Object.assign(document.createElement('div'), { className: "social__container" });
        const icon = Object.assign(document.createElement("div"), { className: `share__icon share__${socialOption.split(" ").join("")}-icon` });
        const socialText = Object.assign(document.createElement("span"), { className: "share__option-text" }, { textContent: `${socialOption}` });
        const shareLink = (socialOption === "Copy Link") ? 
            Object.assign(document.createElement('div'), { role: "button", className: "link-container CopyLink" }) : 
            Object.assign(document.createElement('a'), { className: "link-container" });

       
        if (socialOption === "LinkedIn") {
            shareLink.setAttribute('href', `https://www.linkedin.com/sharing/share-offsite/?url=${window.location.href}`);
            shareLink.setAttribute('target', '_blank');
        }
        if (socialOption === "WhatsApp") {
            shareLink.setAttribute('href', `https://api.whatsapp.com/send?text=${window.location.href}`); 
            shareLink.setAttribute('target', "_blank");
        }

        shareLink.append(icon, socialText);
        socialContainer.append(shareLink);
        document.querySelector(".share__modal").appendChild(socialContainer);

        //adding copy url functionality
        if(socialOption === "Copy Link") {
            shareLink.addEventListener("click", function() {
                var tempInput = document.createElement("input");
                tempInput.value = window.location.href; 
                document.body.appendChild(tempInput); 
                tempInput.select();
                tempInput.setSelectionRange(0, 99999); // For mobile devices
                document.execCommand('copy');
                document.body.removeChild(tempInput);
                this.querySelector(".share__option-text").textContent = "Copied"
            })
        }
    });
    document.querySelector(".hover__share-modal-container").addEventListener("mouseover", () => document.querySelector('[data-gfg-action="share-article"]').classList.add("hover_share_menu"));
}
function toggleLikeElementVisibility(selector, show) {
    document.querySelector(`.${selector}`).style.display = show ? "block" : "none";
}

function closeKebabMenu(){
  document.getElementById("myDropdown").classList.toggle("show");
}
</script>
<!-- Script for the new design of similar read  -->
<script>
$(document).ready(function() {

    $("#showMoreTagsBtn").click(function() {
        $('.articles-hidden-tags').show();
        $(this).hide();
    });

    $("#showMorePracticeTagsBtn").click(function() {
        $(".practice-tags li:nth-child(n+5)").show();
        $(this).hide();
    });
});
</script>
<!-- Script end for similar read -->
<style>
        .grecaptcha-badge {
            visibility: hidden !important;
        }
        .thank-you-message {
            height: 100%;
            display:flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .thank-you-message-content {
            margin-top: 17px;
            font: 400 20px var(--font-secondary);
            color: var(--improve-modal-text);
            line-height: 180%;
            text-align: center;
        }
        .thank-you-message-content h2{
          font-family: var(--font-secondary);
        }
        .all-footer-information{
          width: 100% !important;;
        }
        .footer-wrapper_links-list{
           margin-block-start: 0em !important;
           width: 16% !important; 
           padding-inline-start: 18px !important;
        }
        .link-head{
               margin-bottom: 0px;
        }
        @media only screen and (max-width:1340px) {
              .footer-wrapper_links-list{
              overflow-wrap: break-word;
          }
        }
        @media screen and (min-width: 991px)  {
              .all-footer-information{
                padding-left:15px;
          }
        }
        @media only screen and (max-width:980px) {
          .footer-wrapper_branding-address{
               padding-top: 10px;
          }
        }
        @media (max-width: 750px) {
            .thank-you-message-content{
                font-size: 14px;
                line-height: 170%;
            }
        }

        /* CSS variable meant to handle the dark and light mode icon for three 90 event in header courses dropdown */
        :root{
          --three90headericon : url('https://media.geeksforgeeks.org/auth-dashboard-uploads/three90daylogocompressed.svg');
          --three90headericonposition : 0px -40px;
          --three90leftbarimggrid : url('https://media.geeksforgeeks.org/auth-dashboard-uploads/three90leftbarspritecompressed.svg');
          --three90leftbarimgposition : -5px -55px;
          --three90leftbarbgcolour : #b3abd0;
        }

        body[data-dark-mode="true"]{
          --three90leftbarimgposition : -6px 1px;
          --three90headericonposition : 0px 0px;
          --three90leftbarbgcolour: #8c82b9;
        }

        .three90leftbarimg{
          margin-left: -5px;
          height: 30px;
          background-image: var(--three90leftbarimggrid);
          background-repeat: no-repeat;
          background-position: var(--three90leftbarimgposition);
          background-size: 212px;
        }

        .courseTabShimmer{
          position: absolute;
          height: 110%;
          width: 0;
          opacity: .7;
          -webkit-animation: courseShimmer 2s cubic-bezier(0,0,.07,.61) infinite;
          animation: courseShimmer 2s cubic-bezier(0,0,.07,.61) infinite;
          box-shadow: 0 0 25px 5px #dddcdc;
          -webkit-transform: rotate(90deg);
          transform: rotate(90deg);
          padding:0px !important;
          border:unset !important;
        }

        @keyframes courseShimmer{
          0% {
              left: 0;
          }
          55% {
              left: 100%;
          }
          99% {
              left: 110%;
          }
        }

</style>


	</div><!-- #main .wrapper -->
  <div id="displayModal" class="modal fade" role="dialog">
    <div class="modal-dialog">
      <!-- <div class="upper-box">
        <h3 style="font: normal normal bold 18px/31px var(--font-primary); color: var(--color-black);">Improve your Coding Skills with Practice</h3>
        <button class="upper-box-btn"><a style="color: white !important;" href="https://practice.geeksforgeeks.org/explore?page=1&sortBy=submissions&utm_source=gfg&utm_medium=search-bar&utm_campaign=practice-search">Try It!</a></button>
      </div> -->
      <div class="modal-content">
        <div class="error-message"></div>
        <!-- <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" data-modal="displayModal">&times;</button>
          <h2 class="modal-title" id="dmTitle"></h2>
        </div> -->
        <div class="modal-body" id="dmBody">
            <div id="modal-dm-content"></div>
              <div class="modal-overlay" aria-hidden=true>
                <span class="loader__animation"></span>
              </div>
            <!-- body -->
        </div>
      </div>
    </div>
  </div>  
  <div id="displayModalBackdrop" class="backdrop"></div>
  <!-- Footer start -->
  <footer class="gfg-footer" id="gfg-footer">
      <div class="footer-wrapper">
          <div class="footer-wrapper_branding">
              <a class="footer-wrapper_branding-anchor" aria-label="GeeksforGeeks Logo" href="https://www.geeksforgeeks.org/">
                <img style="height: 32px; width: 230px; max-width: fit-content;" class="footer-wrapper_branding-nlogo" src="https://media.geeksforgeeks.org/auth-dashboard-uploads/gfgFooterLogo.png" alt="geeksforgeeks-footer-logo"/>
              </a>
              <div class="footer-wrapper_branding-address">
                  <div class="address_section">
                    <div class="address-icon-wrapper">
                      <i class="gfg-icon gfg-icon_pin"></i> 
                    <div class="address_div">
                                          <div class="footer-address">
                      Corporate & Communications Address:- A-143, 7th Floor, Sovereign Corporate Tower, Sector- 136, Noida, Uttar Pradesh (201305) | Registered Address:- K 061, Tower K, Gulshan Vivante Apartment, Sector 137, Noida, Gautam Buddh Nagar, Uttar Pradesh, 201305                    </div>
                    </div>
                  </div>
                                      </div>
              </div>
              <div class="footer-wrapper_branding-social">
                  <a href="https://www.facebook.com/geeksforgeeks.org/" rel="noopener noreferrer" aria-label="GeeksforGeeks Facebook" target="_blank">
                      <div class="facebook"></div>
                  </a>
                  <a href="https://www.instagram.com/geeks_for_geeks/" rel="noopener noreferrer" aria-label="GeeksforGeeks Instagram" target="_blank">
                      <div class="instagram"></div>
                  </a>
                  <a href="https://in.linkedin.com/company/geeksforgeeks" rel="noopener noreferrer" aria-label="GeeksforGeeks LinkedIn" target="_blank">
                      <div class="linkedin"></div>
                  </a>
                  <a href="https://twitter.com/geeksforgeeks" rel="noopener noreferrer" aria-label="GeeksforGeeks Twitter" target="_blank">
                      <div class="twitter"></div>
                  </a>
                  <a href="https://www.youtube.com/geeksforgeeksvideos" rel="noopener noreferrer" aria-label="GeeksforGeeks YouTube" target="_blank">
                      <div class="youtube"></div>
                  </a>
              </div>
              <div class="footer-wrapper_branding-app">
                  <a aria-label="GeeksforGeeks App Link" href="https://geeksforgeeksapp.page.link/gfg-app" target="_blank" ><img src="https://media.geeksforgeeks.org/auth-dashboard-uploads/googleplay.png" alt="GFG App on Play Store" id="gplay" loading="lazy"></a>
                  <a aria-label="GeeksforGeeks App Link" href="https://geeksforgeeksapp.page.link/gfg-app" target="_blank"><img src="https://media.geeksforgeeks.org/auth-dashboard-uploads/appstore.png" alt="GFG App on App Store" id="appstore" loading="lazy"></a>
              </div>
          </div> 
        <div class="all-footer-information">
          <div class="footer-wrapper_links" style="justify-content: space-between; text-align: -webkit-left;"><ul class="footer-wrapper_links-list" ><li>Company</li><li><a href=https://www.geeksforgeeks.org/about/?ref=outindfooter>About Us</a></li><li><a href=https://www.geeksforgeeks.org/legal/?ref=outindfooter>Legal</a></li><li><a href=https://www.geeksforgeeks.org/press-release/?ref=outindfooter>In Media</a></li><li><a href=https://www.geeksforgeeks.org/about/contact-us/?ref=outindfooter>Contact Us</a></li><li><a href=https://www.geeksforgeeks.org/advertise-with-us/?ref=outindfooter>Advertise with us</a></li><li><a href=https://www.geeksforgeeks.org/gfg-corporate-solution/?ref=outindfooter>GFG Corporate Solution</a></li><li><a href=https://www.geeksforgeeks.org/campus-training-program/?ref=outindfooter>Placement Training Program</a></li><li><a href=https://www.geeksforgeeks.org/community/?ref=outindfooter>GeeksforGeeks Community</a></li></ul><ul class="footer-wrapper_links-list" ><li><a class="link-head" href=https://www.geeksforgeeks.org/introduction-to-programming-languages/?ref=outindfooter>Languages</a></li><li><a href=https://www.geeksforgeeks.org/python-programming-language/?ref=outindfooter>Python</a></li><li><a href=https://www.geeksforgeeks.org/java/?ref=outindfooter>Java</a></li><li><a href=https://www.geeksforgeeks.org/c-plus-plus/?ref=outindfooter>C++</a></li><li><a href=https://www.geeksforgeeks.org/php-tutorials/?ref=outindfooter>PHP</a></li><li><a href=https://www.geeksforgeeks.org/golang/?ref=outindfooter>GoLang</a></li><li><a href=https://www.geeksforgeeks.org/sql-tutorial/?ref=outindfooter>SQL</a></li><li><a href=https://www.geeksforgeeks.org/r-tutorial/?ref=outindfooter>R Language</a></li><li><a href=https://www.geeksforgeeks.org/android-tutorial/?ref=outindfooter>Android Tutorial</a></li><li><a href=https://www.geeksforgeeks.org/geeksforgeeks-online-tutorials-free/?ref=outindfooter>Tutorials Archive</a></li></ul><ul class="footer-wrapper_links-list" ><li><a class="link-head" href=https://www.geeksforgeeks.org/learn-data-structures-and-algorithms-dsa-tutorial/?ref=outindfooter>DSA</a></li><li><a href=https://www.geeksforgeeks.org/data-structures/?ref=outindfooter>Data Structures</a></li><li><a href=https://www.geeksforgeeks.org/fundamentals-of-algorithms/?ref=outindfooter>Algorithms</a></li><li><a href=https://www.geeksforgeeks.org/complete-guide-to-dsa-for-beginners/?ref=outindfooter>DSA for Beginners</a></li><li><a href=https://www.geeksforgeeks.org/basic-coding-problems-in-dsa-for-beginners/?ref=outindfooter>Basic DSA Problems</a></li><li><a href=https://www.geeksforgeeks.org/complete-roadmap-to-learn-dsa-from-scratch/?ref=outindfooter>DSA Roadmap</a></li><li><a href=https://www.geeksforgeeks.org/top-100-data-structure-and-algorithms-dsa-interview-questions-topic-wise/?ref=outindfooter>Top 100 DSA Interview Problems</a></li><li><a href=https://www.geeksforgeeks.org/dsa-roadmap-for-beginner-to-advanced-by-sandeep-jain/?ref=outindfooter>DSA Roadmap by Sandeep Jain</a></li><li><a href=https://www.geeksforgeeks.org/geeksforgeeks-master-sheet-list-of-all-cheat-sheets/?ref=outindfooter>All Cheat Sheets</a></li></ul><ul class="footer-wrapper_links-list" ><li><a class="link-head" href=https://www.geeksforgeeks.org/ai-ml-ds/?ref=outindfooter>Data Science & ML</a></li><li><a href=https://www.geeksforgeeks.org/data-science-tutorial/?ref=outindfooter>Data Science With Python</a></li><li><a href=https://www.geeksforgeeks.org/data-science-for-beginners/?ref=outindfooter>Data Science For Beginner</a></li><li><a href=https://www.geeksforgeeks.org/machine-learning/?ref=outindfooter>Machine Learning</a></li><li><a href=https://www.geeksforgeeks.org/machine-learning-mathematics/?ref=outindfooter>ML Maths</a></li><li><a href=https://www.geeksforgeeks.org/python-data-visualization-tutorial/?ref=outindfooter>Data Visualisation</a></li><li><a href=https://www.geeksforgeeks.org/pandas-tutorial/?ref=outindfooter>Pandas</a></li><li><a href=https://www.geeksforgeeks.org/numpy-tutorial/?ref=outindfooter>NumPy</a></li><li><a href=https://www.geeksforgeeks.org/natural-language-processing-nlp-tutorial/?ref=outindfooter>NLP</a></li><li><a href=https://www.geeksforgeeks.org/deep-learning-tutorial/?ref=outindfooter>Deep Learning</a></li></ul><ul class="footer-wrapper_links-list" ><li><a class="link-head" href=https://www.geeksforgeeks.org/web-technology/?ref=outindfooter>Web Technologies</a></li><li><a href=https://www.geeksforgeeks.org/html/?ref=outindfooter>HTML</a></li><li><a href=https://www.geeksforgeeks.org/css/?ref=outindfooter>CSS</a></li><li><a href=https://www.geeksforgeeks.org/javascript/?ref=outindfooter>JavaScript</a></li><li><a href=https://www.geeksforgeeks.org/typescript/?ref=outindfooter>TypeScript</a></li><li><a href=https://www.geeksforgeeks.org/learn-reactjs/?ref=outindfooter>ReactJS</a></li><li><a href=https://www.geeksforgeeks.org/nextjs/?ref=outindfooter>NextJS</a></li><li><a href=https://www.geeksforgeeks.org/bootstrap/?ref=outindfooter>Bootstrap</a></li><li><a href=https://www.geeksforgeeks.org/web-design/?ref=outindfooter>Web Design</a></li></ul><ul class="footer-wrapper_links-list" ><li><a class="link-head" href=https://www.geeksforgeeks.org/python-programming-language/?ref=outindfooter>Python Tutorial</a></li><li><a href=https://www.geeksforgeeks.org/python-programming-examples/?ref=outindfooter>Python Programming Examples</a></li><li><a href=https://www.geeksforgeeks.org/python-projects-beginner-to-advanced/?ref=outindfooter>Python Projects</a></li><li><a href=https://www.geeksforgeeks.org/python-tkinter-tutorial/?ref=outindfooter>Python Tkinter</a></li><li><a href=https://www.geeksforgeeks.org/python-web-scraping-tutorial/?ref=outindfooter>Web Scraping</a></li><li><a href=https://www.geeksforgeeks.org/opencv-python-tutorial/?ref=outindfooter>OpenCV Tutorial</a></li><li><a href=https://www.geeksforgeeks.org/python-interview-questions/?ref=outindfooter>Python Interview Question</a></li><li><a href=https://www.geeksforgeeks.org/django-tutorial/?ref=outindfooter>Django</a></li></ul></div><div class="footer-wrapper_links" style="justify-content: space-between; text-align: -webkit-left;"><ul class="footer-wrapper_links-list" style="margin-block-start: 0em; width:16%; padding-inline-start: 18px;"><li>Computer Science</li><li><a href=https://www.geeksforgeeks.org/operating-systems/?ref=outindfooter>Operating Systems</a></li><li><a href=https://www.geeksforgeeks.org/computer-network-tutorials/?ref=outindfooter>Computer Network</a></li><li><a href=https://www.geeksforgeeks.org/dbms/?ref=outindfooter>Database Management System</a></li><li><a href=https://www.geeksforgeeks.org/software-engineering/?ref=outindfooter>Software Engineering</a></li><li><a href=https://www.geeksforgeeks.org/digital-electronics-logic-design-tutorials/?ref=outindfooter>Digital Logic Design</a></li><li><a href=https://www.geeksforgeeks.org/engineering-mathematics-tutorials/?ref=outindfooter>Engineering Maths</a></li><li><a href=https://www.geeksforgeeks.org/software-development/?ref=outindfooter>Software Development</a></li><li><a href=https://www.geeksforgeeks.org/software-testing-tutorial/?ref=outindfooter>Software Testing</a></li></ul><ul class="footer-wrapper_links-list" ><li><a class="link-head" href=https://www.geeksforgeeks.org/devops-tutorial/?ref=outindfooter>DevOps</a></li><li><a href=https://www.geeksforgeeks.org/git-tutorial/?ref=outindfooter>Git</a></li><li><a href=https://www.geeksforgeeks.org/linux-tutorial/?ref=outindfooter>Linux</a></li><li><a href=https://www.geeksforgeeks.org/aws-tutorial/?ref=outindfooter>AWS</a></li><li><a href=https://www.geeksforgeeks.org/docker-tutorial/?ref=outindfooter>Docker</a></li><li><a href=https://www.geeksforgeeks.org/kubernetes-tutorial/?ref=outindfooter>Kubernetes</a></li><li><a href=https://www.geeksforgeeks.org/microsoft-azure/?ref=outindfooter>Azure</a></li><li><a href=https://www.geeksforgeeks.org/google-cloud-platform-tutorial/?ref=outindfooter>GCP</a></li><li><a href=https://www.geeksforgeeks.org/devops-roadmap/?ref=outindfooter>DevOps Roadmap</a></li></ul><ul class="footer-wrapper_links-list" ><li><a class="link-head" href=https://www.geeksforgeeks.org/system-design-tutorial/?ref=outindfooter>System Design</a></li><li><a href=https://www.geeksforgeeks.org/what-is-high-level-design-learn-system-design/?ref=outindfooter>High Level Design</a></li><li><a href=https://www.geeksforgeeks.org/what-is-low-level-design-or-lld-learn-system-design/?ref=outindfooter>Low Level Design</a></li><li><a href=https://www.geeksforgeeks.org/unified-modeling-language-uml-introduction/?ref=outindfooter>UML Diagrams</a></li><li><a href=https://www.geeksforgeeks.org/system-design-interview-guide/?ref=outindfooter>Interview Guide</a></li><li><a href=https://www.geeksforgeeks.org/software-design-patterns/?ref=outindfooter>Design Patterns</a></li><li><a href=https://www.geeksforgeeks.org/object-oriented-analysis-and-design/?ref=outindfooter>OOAD</a></li><li><a href=https://www.geeksforgeeks.org/system-design-interview-bootcamp-guide/?ref=outindfooter>System Design Bootcamp</a></li><li><a href=https://www.geeksforgeeks.org/most-commonly-asked-system-design-interview-problems-questions/?ref=outindfooter>Interview Questions</a></li></ul><ul class="footer-wrapper_links-list" ><li><a class="link-head" href=https://www.geeksforgeeks.org/technical-interview-preparation/?ref=outindfooter>Inteview Preparation</a></li><li><a href=https://www.geeksforgeeks.org/competitive-programming-a-complete-guide/?ref=outindfooter>Competitive Programming</a></li><li><a href=https://www.geeksforgeeks.org/top-algorithms-and-data-structures-for-competitive-programming/?ref=outindfooter>Top DS or Algo for CP</a></li><li><a href=https://www.geeksforgeeks.org/company-wise-recruitment-process/?ref=outindfooter>Company-Wise Recruitment Process</a></li><li><a href=https://www.geeksforgeeks.org/company-preparation/?ref=outindfooter>Company-Wise Preparation</a></li><li><a href=https://www.geeksforgeeks.org/aptitude-questions-and-answers/?ref=outindfooter>Aptitude Preparation</a></li><li><a href=https://www.geeksforgeeks.org/puzzles/?ref=outindfooter>Puzzles</a></li></ul><ul class="footer-wrapper_links-list" ><li>School Subjects</li><li><a href=https://www.geeksforgeeks.org/maths/?ref=outindfooter>Mathematics</a></li><li><a href=https://www.geeksforgeeks.org/physics/?ref=outindfooter>Physics</a></li><li><a href=https://www.geeksforgeeks.org/chemistry/?ref=outindfooter>Chemistry</a></li><li><a href=https://www.geeksforgeeks.org/biology/?ref=outindfooter>Biology</a></li><li><a href=https://www.geeksforgeeks.org/social-science/?ref=outindfooter>Social Science</a></li><li><a href=https://www.geeksforgeeks.org/english-grammar/?ref=outindfooter>English Grammar</a></li><li><a href=https://www.geeksforgeeks.org/commerce/?ref=outindfooter>Commerce</a></li><li><a href=https://www.geeksforgeeks.org/tag/world-general-knowledge/?ref=outindfooter>World GK</a></li></ul><ul class="footer-wrapper_links-list" ><li><a class="link-head" href=https://www.geeksforgeeks.org/videos/?ref=outindfooter>GeeksforGeeks Videos</a></li><li><a href=https://www.geeksforgeeks.org/videos/category/sde-sheet/?ref=outindfooter>DSA</a></li><li><a href=https://www.geeksforgeeks.org/videos/category/python/?ref=outindfooter>Python</a></li><li><a href=https://www.geeksforgeeks.org/videos/category/java-w6y5f4/?ref=outindfooter>Java</a></li><li><a href=https://www.geeksforgeeks.org/videos/category/c/?ref=outindfooter>C++</a></li><li><a href=https://www.geeksforgeeks.org/videos/category/web-development/?ref=outindfooter>Web Development</a></li><li><a href=https://www.geeksforgeeks.org/videos/category/data-science/?ref=outindfooter>Data Science</a></li><li><a href=https://www.geeksforgeeks.org/videos/category/cs-subjects/?ref=outindfooter>CS Subjects</a></li></ul></div>        </div> 
      </div>
            <!-- Jobs Fair 2024 related CSS changes -->

<style>
  :root{
    --home-jobs-section-jf-logo: url('https://media.geeksforgeeks.org/auth-dashboard-uploads/JobFair2024Logo.svg');
  }

  body[data-dark-mode="true"]
  {
    --home-jobs-section-jf-logo: url('https://media.geeksforgeeks.org/auth-dashboard-uploads/JobFair2024LogoDark.svg');
  }

  .hp_job_section_jf_logo, .job-a-thon-jf-sticky-header-logo{
    background: var(--home-jobs-section-jf-logo);
    height: 50px;
    background-repeat: no-repeat;
    width: 105px;
    background-size: 100px;
  }

  @keyframes challenge {
	0%{
		transform: scale(1);
	}
	50%{
		transform: scale(1.03);
	}
	100%{
		transform: scale(1);
	}
  }

  .job-a-thon-jf-sticky-header-logo{
    height: 45px;
  }

</style>

<!-- ---------------------------------- -->
      <div class="footer-strip" >
          <div class="copyright">
              <a href="https://www.geeksforgeeks.org/" rel="noopener noreferrer" target="_blank">@GeeksforGeeks, Sanchhaya Education Private Limited</a><span>, <a href="https://www.geeksforgeeks.org/copyright-information/">All rights reserved</a></span>
          </div>
          <div class="social-links">
          </div>
      </div>
  </footer>
</div><!-- #page -->
<script type='text/javascript' src='https://www.geeksforgeeks.org/wp-includes/js/wp-embed.min.js?ver=4.9.8'></script>

<!-- Cookie Consent Div-->
<div class="cookie-consent hide-consent">
    <span class="cookie-text">
        We use cookies to ensure you have the best browsing experience on our website. By using our site, you
        acknowledge that you have read and understood our
        <a href="https://www.geeksforgeeks.org/cookie-policy/" target="_blank"><u>Cookie Policy</u></a> &
        <a href="https://www.geeksforgeeks.org/privacy-policy/" target="_blank"><u>Privacy Policy</u></a>
            </span>
    <button class="consent-btn">
        Got It !
    </button>
</div>
<!-- Cookie Consent Div ends -->

<!--Light Box Div starts-->
<div class="lightbox-target">
   <img id="lightbox-image" src="" alt="Lightbox"/>
   <span class="lightbox-close"></span>
</div>
<!--Light Box Div ends-->

<!-- <link rel="stylesheet" href="https://use.typekit.net/mrg0hpc.css"/> -->
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<script>
  if(post_slug.includes('premium-plans-payment/') || post_slug.includes('premium-plans/')){
    $('.darkMode-wrap').remove();
    $('.toggle-darkMode').remove();
  }

function setGoogleRecaptcha() {
    var captchaSiteKey = '6LdMFNUZAAAAAIuRtzg0piOT-qXCbDF-iQiUi9KY';
    grecaptcha.ready(function() {
        grecaptcha.execute(captchaSiteKey).then(function(token) {
            document.getElementById('g-recaptcha-response-suggestion-form').value = token;
            suggestionCall();
        });
    });
}

</script>

        <div class="improve-modal--overlay" style="display: none;">
            <div class="improve-modal--improvement" status="locked">
                <div class="improve-modal--improve-header">
                    <div class="improve-header-fst-child">Improvement</div>
                    <div class="improve-header-sec-child">
                        <i class="gfg-icon improve-cross-icon"></i>
                    </div>
                </div>
                <div class="locked-status--impove-modal">
                    <div class="improve-modal--improve-content error-message"></div>                    
                    <div class="improve-modal--improve-bottom">
                        <button class="improve-bottom-btn" type="button">Suggest changes</button>
                    </div>
                </div>
                <div class="unlocked-status--improve-modal-content">
                  <div class="suggest-change_wrapper">
                    <div class="suggest-change-content_wrapper">
                      <div class="suggest-change">Suggest Changes</div>
                      <div class="suggest-changes-about">Help us improve. Share your suggestions to enhance the article. Contribute your expertise and make a difference in the GeeksforGeeks portal.</div>
                    </div>
                    <div class="suggest-change-icon_wrapper">
                      <img class="suggest-change-icon" src="https://media.geeksforgeeks.org/auth-dashboard-uploads/suggestChangeIcon.png" alt="geeksforgeeks-suggest-icon"/>
                    </div>
                  </div>
                  <div class="create-improvement_wrapper">
                    <div class="create-improvement-content_wrapper">
                      <div class="create-improvement">Create Improvement</div>
                      <div class="create-improvements-about">Enhance the article with your expertise. Contribute to the GeeksforGeeks community and help create better learning resources for all.</div>
                    </div>
                    <div class="create-improvement-icon_wrapper">
                    <img class="create-improvement-icon" src="https://media.geeksforgeeks.org/auth-dashboard-uploads/createImprovementIcon.png" alt="geeksforgeeks-improvement-icon"/>
                    </div>
                  </div>
                  <div class="error-status"></div>
                </div>
            </div>
            <div class="improve-modal--suggestion" style="display: none;">
                <!-- Header of improve-modal--improvement and improve-modal--suggestion have same CSS rule that's why I use same class name -->
                <div class="improve-modal--improve-header">
                  <div class="left-arrow-icon_suggest_wrapper">
                    <div class="left-arrow-icon_wrapper">
                      <i class="gfg-icon improve-left-arrow-icon"></i>
                    </div>
                    <div class="improve-header-fst-child">Suggest Changes</div>
                  </div>
                  <div class="improve-header-sec-child">
                        <i class="gfg-icon improve-cross-icon"></i>
                  </div>
                </div>
                <div class="suggestion-modal-section">
                    <form>
                        <label for="suggestion-section">min 4 words, max CharLimit:2000</label>
                        <textarea id="suggestion-section-textarea" name="suggestion-section" placeholder="Write your suggestions here"></textarea>
                        <input type="hidden" name="g-recaptcha-suggestion-response" id="g-recaptcha-response-suggestion-form">
                    </form>
                </div> 
                <!-- Button of improve-modal--improvement and improve-modal--suggestion have same CSS rule that's why I use same class name -->
                <div class="improve-modal--improve-bottom suggestion-btn">
                    <p><span id="suggestion-modal-alert" style="display: none;"></span></p>
                    <button class="suggest-bottom-btn" type="button"></button>
                </div>
            </div>
            <a href="#" style="visibility:hidden" class="create-improvement-redirection-to-write" target="_blank"></a>
        </div>
        <script>
            var lockedCasesHtml = `<span class="improve-modal--improve-content-modified"></span><span>You can suggest the changes for now and it will be under 'My Suggestions' Tab on Write.</span><br><br><span>You will be notified via email once the article is available for improvement. Thank you for your valuable feedback!</span>`;
            var badgesRequiredHtml = `<span>It seems that you do not meet the eligibility criteria to create improvements for this article, as only users who have earned specific badges are permitted to do so.</span><br><br><span>However, you can still create improvements through the <a href="https://write.geeksforgeeks.org/pick-improvements/pick" target='_blank'>Pick for Improvement</a> section.</span>`;
            jQuery('.improve-header-sec-child').on('click', function(){
                jQuery('.improve-modal--overlay').hide();
                $('.improve-modal--suggestion').hide();
            });

            $('.suggest-change_wrapper, .locked-status--impove-modal .improve-bottom-btn').on('click',function(){ // when suggest changes option is clicked
              $('#suggestion-section-textarea').val("");
              $('.suggest-bottom-btn').html("Suggest changes");
              $('.improve-modal--improvement').hide();
              $('.improve-modal--suggestion').show();
            });
            $('.create-improvement_wrapper').on('click',function(){  // when create improvement option clicked then improvement reason will be shown
              if(loginData && loginData.isLoggedIn) {
                $('body').append('<div class="spinner-loading-overlay"></div>');
                $('.spinner-loading-overlay').show();
                jQuery.ajax({
                  url: writeApiUrl + 'create-improvement-post/?v=1',
                  type: "POST",
                  contentType: 'application/json; charset=utf-8',
                  dataType: 'json',
                  xhrFields: {
                    withCredentials: true
                  },
                  data: JSON.stringify({
                    gfg_id: post_id
                  }),
                  success:function(result) {
                    $('.spinner-loading-overlay:eq(0)').remove();
                    $('.improve-modal--overlay').hide();
                    $('.unlocked-status--improve-modal-content').css("display","none");
                    $('.create-improvement-redirection-to-write').attr('href',writeUrl + 'improve-post/' + `${result.id}` + '/', '_blank');
                    $('.create-improvement-redirection-to-write')[0].click();
                  },
                  error:function(e) {
                    showErrorMessage(e.responseJSON,e.status)
                  },
                });
              }
              else {
               if(loginData && !loginData.isLoggedIn) {
                   $('.improve-modal--overlay').hide();
                if ($('.header-main__wrapper').find('.header-main__signup.login-modal-btn').length) {
                $('.header-main__wrapper').find('.header-main__signup.login-modal-btn').click();
                 }
                return;
                }
              }
            });
            $('.left-arrow-icon_wrapper').on('click',function(){
              if($('.improve-modal--suggestion').is(":visible"))
              $('.improve-modal--suggestion').hide();
              else{
              }

              $('.improve-modal--improvement').show();
            });
            const showErrorMessage = (result,statusCode) => {
                if(!result)
                return;
                $('.spinner-loading-overlay:eq(0)').remove();
                if(statusCode == 403) {
                    $('.improve-modal--improve-content.error-message').html(result.message);
                    jQuery('.improve-modal--overlay').show();
                    jQuery('.improve-modal--improvement').show();
                    $('.locked-status--impove-modal').css("display","block");
                    $('.unlocked-status--improve-modal-content').css("display","none");
                    $('.improve-modal--improvement').attr("status","locked");
                    return;
                }
                            }
            function loadScript(src, callback) {
                var script = document.createElement('script');
                script.src = src;
                script.onload = callback;
                document.head.appendChild(script);
            }
            function suggestionCall() {              
                var suggest_val = $.trim($("#suggestion-section-textarea").val());
                var array_String= suggest_val.split(" ") 
                var gCaptchaToken = $("#g-recaptcha-response-suggestion-form").val();
                var error_msg = false;
                if(suggest_val != "" && array_String.length >=4){
                    if(suggest_val.length <= 2000){
                        var payload = {
                                    "gfg_post_id" : `${post_id}`,
                                    "suggestion" : `<p>${suggest_val}</p>`,
                                }
                        if(!loginData || !loginData.isLoggedIn)                  // User is not logged in
                        payload["g-recaptcha-token"] = gCaptchaToken

                        jQuery.ajax({
                            type:'post',
                            url:  "https://apiwrite.geeksforgeeks.org/suggestions/auth/create/",
                            xhrFields: {
                                withCredentials: true
                            },
                            crossDomain: true,
                            contentType:'application/json',
                            data: JSON.stringify(payload),
                            success:function(data) {
                                jQuery('.spinner-loading-overlay:eq(0)').remove();
                                jQuery('#suggestion-section-textarea').val("");
                                jQuery('.suggest-bottom-btn').css("display","none");
                                
                                // Update the modal content
                                const modalSection = document.querySelector('.suggestion-modal-section');
                                modalSection.innerHTML = `
                                    <div class="thank-you-message" style="text-align: center;">
                                      <h2>Thank You!</h2>
                                      <div class="thank-you-message-content">Your suggestions are valuable to us.</div>
                                    </div>
                                `;

                            },
                            error:function(data) {
                                jQuery('.spinner-loading-overlay:eq(0)').remove();
                                jQuery('#suggestion-modal-alert').html("Something went wrong.");
                                jQuery('#suggestion-modal-alert').show();
                                error_msg = true;
                            }
                        });
                    }
                    else{
                        jQuery('.spinner-loading-overlay:eq(0)').remove();
                        jQuery('#suggestion-modal-alert').html("Minimum 5 Words and Maximum Character limit is 2000.");
                        jQuery('#suggestion-modal-alert').show();
                        jQuery('#suggestion-section-textarea').focus();
                        error_msg = true;
                    }
                }
                else{
                    jQuery('.spinner-loading-overlay:eq(0)').remove();
                    jQuery('#suggestion-modal-alert').html("Enter atleast four words !");
                    jQuery('#suggestion-modal-alert').show();
                    jQuery('#suggestion-section-textarea').focus();
                    error_msg = true;
                }
                if(error_msg){
                    setTimeout(() => {
                        jQuery('#suggestion-section-textarea').focus();
                        jQuery('#suggestion-modal-alert').hide();
                    }, 3000);
                }
            }
            
            document.querySelector('.suggest-bottom-btn').addEventListener('click', function(){
              jQuery('body').append('<div class="spinner-loading-overlay"></div>');
              jQuery('.spinner-loading-overlay').show();
              if(loginData && loginData.isLoggedIn) {
                 suggestionCall();
                 return;
              }
              // load the captcha script and set the token
              loadScript('https://www.google.com/recaptcha/api.js?render=6LdMFNUZAAAAAIuRtzg0piOT-qXCbDF-iQiUi9KY',[], function() {
                setGoogleRecaptcha();
              });
            });
            
            $('.improvement-bottom-btn.create-improvement-btn').click(function() {  //create improvement button is clicked
              $('body').append('<div class="spinner-loading-overlay"></div>');
              $('.spinner-loading-overlay').show();
              // send this option via create-improvement-post api
              jQuery.ajax({
                url: writeApiUrl + 'create-improvement-post/?v=1',
                type: "POST",
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                xhrFields: {
                  withCredentials: true
                },
                data: JSON.stringify({
                  gfg_id: post_id
                }),
                success:function(result) {
                  $('.spinner-loading-overlay:eq(0)').remove();
                  $('.improve-modal--overlay').hide();
                  $('.create-improvement-redirection-to-write').attr('href',writeUrl + 'improve-post/' + `${result.id}` + '/', '_blank');
                  $('.create-improvement-redirection-to-write')[0].click();
                },
                error:function(e) {
                  showErrorMessage(e.responseJSON,e.status);
                },
              });
            });
        </script>
    <script>
var AdblockPlus = new function() {
     this.detect = function(px, callback) {
         var detected = false;
         var checksRemain = 2;
         var error1 = false;
         var error2 = false;
         if (typeof callback != "function") return;
         px += "?ch=*&rn=*";

         function beforeCheck(callback, timeout) {
             if (checksRemain == 0 || timeout > 1E3) callback(checksRemain == 0 && detected);
             else setTimeout(function() {
                 beforeCheck(callback, timeout * 2)
             }, timeout * 2)
         }

         function checkImages() {
             if (--checksRemain) return;
             detected = !error1 && error2
         }
         var random = Math.random() * 11;
         var img1 = new Image;
         img1.onload = checkImages;
         img1.onerror = function() {
             error1 = true;
             checkImages()
         };
         img1.src = px.replace(/\*/, 1).replace(/\*/, random);
         var img2 = new Image;
         img2.onload = checkImages;
         img2.onerror = function() {
             error2 = true;
             checkImages()
         };
         img2.src = px.replace(/\*/, 2).replace(/\*/, random);
         beforeCheck(callback, 250)
     }
 };

/*
AdblockPlus.detect("https://cdnads.geeksforgeeks.org/res/px.gif", function(abp){
    window.googletag = window.googletag || {cmd: []};
    window.abp=abp;
    var elms = [...document.querySelectorAll('div[id^=_GFG_ABP_]')];
    const units=elms.map(elem=>elem.id)
    if(abp) {
        for(let curr_unit of units) {
            const iframe = document.createElement('iframe');
            iframe.setAttribute('src',"https://aa.geeksforgeeks.org/iframe.html?code="+curr_unit.substr(1))
            const elem = document.getElementById(curr_unit)
            const div = document.createElement('div');
            div.setAttribute('id',curr_unit.substr(1))
            let sizes = curr_unit.split("_");
            sizes = sizes.filter(val => val.includes('x'));
            let [width, height] = sizes[0].split("x");
            iframe.style.width = `${+width+20}px`
            iframe.style.height = `${+height+20}px`
            if(elem) {
                elem.appendChild(iframe);
            }
        }
        var gfgAdDivs = [...document.querySelectorAll('div[id^=GFG_AD_]')];
        gfgAdDivs.forEach(gfgDiv => document.getElementById(gfgDiv.id).removeAttribute("style"));
        jQuery('#secondary .widget_text:last-child').css({"position": "unset"});
    }
});*/
    AdblockPlus.detect("https://cdnads.geeksforgeeks.org/res/px.gif", function(abp){
    window.googletag = window.googletag || {cmd: []};
    window.abp=abp;
    var elms = [...document.querySelectorAll('div[id^=_GFG_ABP_]')];
    //const units=elms.map(elem=>elem.id)
    const units = elms
      .filter(elem => !(window.innerWidth < 1500 && elem.id === "_GFG_ABP_Incontent_728x90"))
      .map(elem => elem.id);
    if(abp) {
        isAdBlockerPresent = true;
        for(let curr_unit of units) {
            const iframe = document.createElement('iframe');
            iframe.addEventListener("load", () => {
              iframe.contentWindow.postMessage(JSON.stringify({host: window.location.host,category: window.arrPostCatName,parentWidth: window.innerWidth}),'https://aa.geeksforgeeks.org');
            });
            iframe.setAttribute('src',"https://aa.geeksforgeeks.org/iframe.html?code="+curr_unit.substr(1))
            const elem = document.getElementById(curr_unit)
            const div = document.createElement('div');
            div.setAttribute('id',curr_unit.substr(1))
            let sizes = curr_unit.split("_");
            sizes = sizes.filter(val => val.includes('x'));
            let [width, height] = sizes[0].split("x");
            iframe.style.width = `${+width+20}px`
            iframe.style.height = `${+height+20}px`
            if(elem) {
                elem.appendChild(iframe);
            }
        }
        var gfgAdDivs = [...document.querySelectorAll('div[id^=GFG_AD_]')];
        gfgAdDivs.forEach(gfgDiv => document.getElementById(gfgDiv.id).removeAttribute("style"));
        jQuery('#secondary .widget_text:last-child').css({"position": "unset"});
    }
    else{
      try {
        var isAdblockEnabled = t =>
            fetch(
                new Request('https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js', {
                    method: 'HEAD',
                    mode: 'no-cors'
                })
            ).catch(t);
          isAdblockEnabled(() => {
            // here goes modal pop-up code
            isAdBlockerPresent = true;
          });
      } catch (err) {console.log(err);}
    }
});

  function closeAdBlockPopupModal(){
    const modal = document.getElementById("adBlockerModal");
    $('body').removeClass('body-for-ad-blocker');
    $('#adBlockerModal').remove()
    localStorage.setItem('gfgAdBlockPopup',new Date())
  }
  function showAdblockerModal(){
    let randomNumberForButtonText = Math.round(Math.random()); 
    let currTime = new Date();
    let lastTime = new Date(localStorage.getItem('gfgAdBlockPopup'));
    if(((currTime-lastTime)/(1000*60*60))<1)
    {
      return;
    }
    const adBlockerModal = `<div id="adBlockerModal" class="ad-blocker-modal">
      <div id="ad-blocker-modal-overlay">
        <div id="ad-blocker-outer-div">
          <div id="ad-blocker-div">
          <p id="ad-blocker-div-warning" style="margin-bottom: 30px;">It seems that you are using an ad blocker.<br><span style="font-size: 22px;font-weight: normal;">Please disable it to support us!</span></p>
              <div id="ad-blocker-div-btns">
                  <button id="ad-blocker-div-button1" onclick="handleAdBlockerClick('disabled')">
                      I disabled my ad blocker
                  </button>
                  <a href="https://www.geeksforgeeks.org/geeksforgeeks-premium-subscription${randomNumberForButtonText === 1 ? "/?itm_source=geeksforgeeks&itm_medium=adblocker&itm_campaign=premium1" : "/?itm_source=geeksforgeeks&itm_medium=adblocker&itm_campaign=premium2"}" target="_blank">
                      <button
                          id="ad-blocker-div-button2"
                          style="
                              background: linear-gradient(45deg, #f0bd36, #bf873f);
                              border: 1px solid transparent;
                              color: white;
                          "
                      >
                          ${randomNumberForButtonText === 1 ? "Go Ad-Free with Premium" : "Upgrade for No Ads"}
                      </button>
                  </a>
              </div>
              <div id="ad-blocker-div-continue-premium-promo-text">
                  "For an ad-free experience and exclusive features, subscribe to our Premium Plan!"<br>
              </div>
              <div id="ad-blocker-div-continue-btn-div">
                  <a id="ad-blocker-div-continue-btn" href="#" onclick="closeAdBlockPopupModal()">Continue without supporting</a>
              </div>
          </div>
        </div>
      </div>
    </div>`;
    $('body').append(adBlockerModal);
    $('body').addClass('body-for-ad-blocker');
    const modal = document.getElementById("adBlockerModal");
    modal.style.display = "block";
  }
  function handleAdBlockerClick(type){
      if(type == 'disabled'){
        window.location.reload();
      }
      else if(type == 'info'){
        document.getElementById("ad-blocker-div").style.display = "none";
        document.getElementById("ad-blocker-info-div").style.display = "flex";
        handleAdBlockerIconClick(0);
      }
  }
  var lastSelected= null;
  //Mapping of name and video URL with the index.
  const adBlockerVideoMap = [
    ['Ad Block Plus','https://media.geeksforgeeks.org/auth-dashboard-uploads/abp-blocker-min.mp4'],
    ['Ad Block','https://media.geeksforgeeks.org/auth-dashboard-uploads/Ad-block-min.mp4'],
    ['uBlock Origin','https://media.geeksforgeeks.org/auth-dashboard-uploads/ub-blocke-min.mp4'],
    ['uBlock','https://media.geeksforgeeks.org/auth-dashboard-uploads/U-blocker-min.mp4'],
  ]
  function handleAdBlockerIconClick(currSelected){
    const videocontainer = document.getElementById('ad-blocker-info-div-gif');
    const videosource = document.getElementById('ad-blocker-info-div-gif-src');
    if(lastSelected != null){
      document.getElementById("ad-blocker-info-div-icons-"+lastSelected).style.backgroundColor = "white";  
      document.getElementById("ad-blocker-info-div-icons-"+lastSelected).style.borderColor = "#D6D6D6";
    }
    document.getElementById("ad-blocker-info-div-icons-"+currSelected).style.backgroundColor = "#D9D9D9";
    document.getElementById("ad-blocker-info-div-icons-"+currSelected).style.borderColor = "#848484";
    document.getElementById('ad-blocker-info-div-name-span').innerHTML = adBlockerVideoMap[currSelected][0]
    videocontainer.pause();
    videosource.setAttribute('src', adBlockerVideoMap[currSelected][1]);
    videocontainer.load();
    videocontainer.play();
    lastSelected = currSelected;
  }
</script>
<!-- <script async src="https://www.googleoptimize.com/optimize.js?id=OPT-5PGZ8MN"></script> -->

<style>
/* Temporary CSS for Three90 pop up modal (START)*/
    .three90popup__container {
      width: 100vw;
      height: 100vh; 
      position: fixed;
      top:0px;
      background: var(--job-tab-faded-background);
      z-index: 1024;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .three90modal__wrapper{
      background-color: white;
      max-width: 350px;
      display: flex;
      flex-direction: column;
      border-radius: 10px;
      overflow: hidden;

    }
    .three90modal__message-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      font-family: var(--font-primary);
    }
    .three90modal__subheading {
      margin-top: 20px;
      font-size: 22px;
      font-weight: 600;
    }
    .three90modal__text-message {
      margin-top: 20px;
      font-size: 15px;
      font-weight: 400;
      text-align: center;
      padding: 0 5px;
    }
    .three90__modal__button-wrapper {
      width: 100%;
      padding: 20px 0px;
      display: flex;
      justify-content: space-evenly;
    }
    .three90__modal__button-wrapper > button {
      width: 105px;
      height: 35px;
      border-radius: 13px;
      border:none;
      font-weight: 600;
      cursor: pointer;
    } 
    #three90__modal-close-btn:hover {
      background-color: #cacbcd;
    }
    #three90__modal-explore-btn {
      background-color: #0a0727;
      color: white
    }

    @media screen and (max-width: 441px) {
      .three90modal__wrapper {
        max-width: 300px;
      }
    }

  /* Temporary CSS for Three90 pop up modal (END)*/
</style>

<script type="text/javascript" >
    const coursePromotionCities = JSON.parse(`{"NCR":{"LOCATIONS":["Noida","Greater Noida","Ghaziabad","Faridabad","Delhi","New Delhi"],"COURSES":[{"name":"GATE CS 2025 Classroom Program","url":"https:\/\/www.geeksforgeeks.org\/courses\/gate-cs-self-paced"},{"name":"MERN Full Stack Development","url":"https:\/\/www.geeksforgeeks.org\/courses\/mern-full-stack-development-classroom"},{"name":"DSA For Interview Preparation","url":" https:\/\/www.geeksforgeeks.org\/courses\/dsa-interview-preparation-classroom"},{"name":"JAVA Backend Development","url":"https:\/\/www.geeksforgeeks.org\/courses\/complete-java-backend-development-program"},{"name":"Data Analytics Programme","url":"https:\/\/www.geeksforgeeks.org\/courses\/complete-data-analytics-program"},{"name":"AWS Solutions Architect Certification","url":"https:\/\/www.geeksforgeeks.org\/courses\/aws-solutions-architect-certification-classroom-training"},{"name":"Explore All","url":"https:\/\/www.geeksforgeeks.org\/courses\/offline-courses"}]},"NON_NCR":{"Bengaluru":[{"name":"Data Science Classroom Program","url":"https:\/\/www.geeksforgeeks.org\/courses\/data-science-classroom-program"},{"name":"System Design Classroom Program","url":"https:\/\/www.geeksforgeeks.org\/courses\/system-design-classroom-program"},{"name":"MERN Full Stack Development","url":"https:\/\/www.geeksforgeeks.org\/courses\/mern-full-stack-development-classroom"},{"name":"DSA For Interview Preparation","url":"https:\/\/www.geeksforgeeks.org\/courses\/dsa-interview-preparation-classroom"},{"name":"JAVA Backend Development","url":"https:\/\/www.geeksforgeeks.org\/courses\/complete-java-backend-development-program"},{"name":"Data Analytics Programme","url":"https:\/\/www.geeksforgeeks.org\/courses\/complete-data-analytics-program"},{"name":"AWS Solutions Architect Certification","url":"https:\/\/www.geeksforgeeks.org\/courses\/aws-solutions-architect-certification-classroom-training"},{"name":"Explore All","url":"https:\/\/www.geeksforgeeks.org\/courses\/offline-courses"}],"Pune":[{"name":"MERN Full Stack Development","url":"https:\/\/www.geeksforgeeks.org\/courses\/mern-full-stack-development-classroom"},{"name":"DSA For Interview Preparation","url":"https:\/\/www.geeksforgeeks.org\/courses\/dsa-interview-preparation-classroom"},{"name":"Complete Data Analytics Program","url":"https:\/\/www.geeksforgeeks.org\/courses\/complete-data-analytics-program"},{"name":"Explore All","url":"https:\/\/www.geeksforgeeks.org\/courses\/offline-courses"}]}}`);
    const offlineCourseTermMapper = JSON.parse(`{"ALL_TERMIDS":["2058","6263","2628","1745","1789","2601","2057","5037","2971","2023","2162","2795"],"COURSE_TERMID_MAP":{"JAVA":["2058"],"DATA_ANALYTICS":["1745","1789","2601","2057","5037","2971","2023","2162","2795"],"DSA":["6263"],"MERN":["2628"]}}`);
</script>

  
<!-- gfg tabs compatablity bundled js -->

<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-KDVRCT5');</script>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DWCCJLKX3X"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
//  gtag('config', 'AW-474915276');
  gtag('config', 'G-DWCCJLKX3X');
  gtag('config', 'AW-796001856');
</script>

<!-- fancybar ad code start -->
<div id="GFG_AD_Desktop_Stickyunit_1x1"></div>
<!-- fancybar ad code ends -->
<!-- <div id="GFG_AD_gfg_mobile_320x50"></div> -->
<style>
    :root {
        --com-extra-icons-mobile-image: url(https://media.geeksforgeeks.org/auth-dashboard-uploads/Com-Extra-Icons13.svg);
        --write-experience-card-1: #ECF5F5;
        --write-experience-card-icon-1: #21898C;
        --write-experience-card-2: #EAF2F7;
        --write-experience-card-icon-2: #3079AC;
        --write-experience-card-3: #FDEFE6;
        --write-experience-card-icon-3: #F5A572;
        --write-experience-card-4: #F1F8F5;
        --write-experience-card-icon-4: #91C4AD;
        --write-experience-card-5: #EEE7FF;
        --write-experience-card-icon-5: #8B72C9;
        --write-experience-card-6: #F2F8E6;
        --write-experience-card-icon-6: #78C57F;
        --editor-button-text-color: #6E6E73;
        --write-modal-background: #fefefe;
        --experience-sidebar: #000;
        --left-bar-background: #FFFFFF;
        --write-redirect-container:#EAF2F7;
        --write-redirect-container-hover:#d6e7f2;
        
    }

    /* Dark Mode */
    body[data-dark-mode="true"] {
        --write-modal-background: #161c23;
        --experience-sidebar: #000;
        --left-bar-background: #F0F3F5;
    }

    .popup-main {
        padding: 20px 18px 20px 18px;
        border-radius: 8px;
    }

    .popup-main .popup-heading {
        display: flex;
        align-items: center;
        color: #E9E9EA;
        margin-bottom: 10px;
        justify-content: space-between;
    }

    .popup-main .close-icon {
        background-image: var(--com-extra-icons-mobile-image);background-position: -15px -1651px;height: 22px;width: 22px;transform: scale(1);
        margin-bottom: 12px;
        cursor: pointer;
    }

    .popup-main .experience-card {
        color: #000;
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        /* margin-bottom:10px; */
    }

    .popup-main a:hover,
    .popup-main a:active,
    .popup-main a:visited {
        color: inherit;
        text-decoration: none;
    }

    .popup-main .exp-card1,
    .popup-main .exp-card2,
    .popup-main .exp-card3,
    .popup-main .exp-card4,
    .popup-main .exp-card5,
    .popup-main .exp-card6 {
        display: flex;
        align-items: center;
        border-radius: 10px;
        cursor: pointer;
    }

    .popup-main .exp-card1 .icon1,
    .popup-main .exp-card2 .icon2,
    .popup-main .exp-card3 .icon3,
    .popup-main .exp-card4 .icon4,
    .popup-main .exp-card5 .icon5,
    .popup-main .exp-card6 .icon6 {
        width: 80px;
        height: 80px;
        border-radius: 10px 0px 0px 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--write-experience-card-icon-1);
    }

    .popup-main .exp-card1 .icon1,
    .popup-main .exp-card2 .icon2,
    .popup-main .exp-card3 .icon3,
    .popup-main .exp-card4 .icon4,
    .popup-main .exp-card5 .icon5,
    .popup-main .exp-card6 .icon6 {
        width: 80px;
        height: 80px;
        border-radius: 10px 0px 0px 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .popup-main .exp-card1 .icon1 {
        background: var(--write-experience-card-icon-1);
    }

    .popup-main .exp-card2 .icon2 {
        background: var(--write-experience-card-icon-2);
    }

    .popup-main .exp-card3 .icon3 {
        background: var(--write-experience-card-icon-3);
    }

    .popup-main .exp-card4 .icon4 {
        background: var(--write-experience-card-icon-4);
    }

    .popup-main .exp-card5 .icon5 {
        background: var(--write-experience-card-icon-5);
    }

    .popup-main .exp-card6 .icon6 {
        background: var(--write-experience-card-icon-6);
    }

    .popup-main .exp-card6 .icon6-image {
        background-image: url(https://media.geeksforgeeks.org/auth-dashboard-uploads/compass.svg);
        width: 46px;
        height: 30px;
        background-size: 30px;
        background-repeat: no-repeat;
        background-position: center;
    }

    .popup-main .exp-card1 .icon1-image {
        background-image: var(--com-extra-icons-mobile-image);
        width: 46px;
        height: 28px;
        background-position: -4px -812px;
    }

    .popup-main .exp-card2 .icon2-image {
        background-image: var(--com-extra-icons-mobile-image);
        width: 46px;
        height: 28px;
        background-position: -4px -888px;
    }

    .popup-main .exp-card3 .icon3-image {
        background-image: var(--com-extra-icons-mobile-image);
        width: 46px;
        height: 28px;
        background-position: -4px -848px;
    }

    .popup-main .exp-card4 .icon4-image {
        background-image: url(https://media.geeksforgeeks.org/auth-dashboard-uploads/competitive.svg);
        width: 46px;
        height: 30px;
        background-size: 30px;
        background-repeat: no-repeat;
        background-position: center;
    }

    .popup-main .exp-card5 .icon5-image {
        background-image: var(--com-extra-icons-mobile-image);
        width: 46px;
        height: 33px;
        background-position: -4px -1217px;
    }


    .popup-main .exp-card1 .exp-card1-text,
    .popup-main .exp-card2 .exp-card2-text,
    .popup-main .exp-card3 .exp-card3-text,
    .popup-main .exp-card4 .exp-card4-text,
    .popup-main .exp-card5 .exp-card5-text,
    .popup-main .exp-card6 .exp-card6-text {
        display: flex;
        align-items: center;
        border-radius: 0px 10px 10px 0px;
        height: 80px;
        width: calc(100% - 80px);
    }

    .popup-main .exp-card1 {
        justify-content: flex-start;
        background: var(--write-experience-card-1);
    }

    .popup-main .exp-card2 {
        justify-content: flex-start;
        background: var(--write-experience-card-2);
    }

    .popup-main .exp-card3 {
        justify-content: flex-start;
        background: var(--write-experience-card-3);
    }

    .popup-main .exp-card4 {
        justify-content: flex-start;
        background: var(--write-experience-card-4);
    }

    .popup-main .exp-card5 {
        justify-content: flex-start;
        background: var(--write-experience-card-5);
    }

    .popup-main .exp-card6 {
        justify-content: flex-start;
        background: var(--write-experience-card-6);
    }

    .popup-main span {
        font-family: var(--font-primary);
        font-size: 14px;
        font-style: normal;
        font-weight: 500;
        line-height: normal;
        padding-left: 5px;
        padding-right: 5px;
    }

    #popup {
        display: none;
        background-color: var(--write-modal-background);
        padding: 20px;
        text-align: center;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1026;
        width: min(650px, calc(100% - 20px));
    }
    .link-container-write{
        display:flex;
        flex-direction:column;
    }
    .link-container-write > a {
        margin:7px 0px;
    }
    .phrase__container{
        color:var(--color-gfg);
        border-radius: 6px;
        width: 100%;
        background-color:var(--write-redirect-container);
        padding: 15px;
        text-align: justify;
        font-size:14px;
    }
    .phrase__container:hover {
        color:var(--color-gfg) !important;
        background-color:var(--write-redirect-container-hover);
    }
</style>
<div class="popup-container">
        <div id="popup" accesskey="" class="popup-main">
            <div class="popup-heading">
                <h2>What kind of Experience do you want to share?</h2>
                <div class="close-icon share-experience-modal-close"></div>
            </div>
            <!-- <span class="description"style="color: #BEBEC2;">Tell us your type of experiences which can help other fellow Geeks for their future events and preparations.</span> -->
            <div class="experience-card">
                <a class="exp-card5" href= "https://write.geeksforgeeks.org/posts-new?cid=e8fc46fe-75e7-4a4b-be3c-0c862d655ed0" target="_blank">
                    <div class="icon5">
                        <div class="icon5-image"></div>
                    </div>
                    <div class="exp-card5-text">
                        <span style="color: #000;">Interview Experiences</span>
                    </div>
                </a>
                <a class="exp-card1" href="https://write.geeksforgeeks.org/posts-new?cid=82536bdb-84e6-4661-87c3-e77c3ac04ede" target="_blank">
                    <div class="icon1">
                        <div class="icon1-image"></div>
                    </div>
                    <div class="exp-card1-text">
                        <span style="color: #000;">Admission Experiences</span>
                    </div>
                </a>
                <a class="exp-card6" href= "https://write.geeksforgeeks.org/posts-new?cid=5219b0b2-7671-40a0-9bda-503e28a61c31" target="_blank">
                    <div class="icon6">
                        <div class="icon6-image"></div>
                    </div>
                    <div class="exp-card6-text">
                        <span style="color: #000;">Career Journeys</span>
                    </div>
                </a>
                <a class="exp-card2" href="https://write.geeksforgeeks.org/posts-new?cid=22ae3354-15b6-4dd4-a5b4-5c7a105b8a8f" target="_blank">
                    <div class="icon2">
                        <div class="icon2-image"></div>
                    </div>
                    <div class="exp-card2-text">
                        <span style="color: #000;">Work Experiences</span>
                    </div>
                </a>
                <a class="exp-card3" href= "https://write.geeksforgeeks.org/posts-new?cid=c5e1ac90-9490-440a-a5fa-6180c87ab8ae" target="_blank">
                    <div class="icon3">
                        <div class="icon3-image"></div>
                    </div>
                    <div class="exp-card3-text">
                        <span style="color: #000;">Campus Experiences</span>
                    </div>
                </a>
                <a class="exp-card4" href= "https://write.geeksforgeeks.org/posts-new?cid=5ebb8fe9-b980-4891-af07-f2d62a9735f2" target="_blank">
                    <div class="icon4">
                        <div class="icon4-image"></div>
                    </div>
                    <div class="exp-card4-text">
                        <span style="color: #000;">Competitive Exam Experiences</span>
                    </div>
                </a>
            </div>
        <!--    <div class="link-container-write">
                <a href="https://write.geeksforgeeks.org/pick-article?taxonomy=10261&page=1">
                    <div role="span" class="phrase__container">
                        Can't choose a topic to write? click here for suggested topics
                    </div>
                </a>
                <a href="https://write.geeksforgeeks.org/posts-new">
                    <div role="span" class="phrase__container">
                       Write and publish your own Article
                    </div>
                </a>
            </div> -->
        </div>
        <div id="overlay" onclick="toggleExperiencePopup()" style="display: block;min-height: 100vh;min-width: 100vw;position: fixed;top: 0;bottom: 0;right: 0;left: 0;display: none;justify-content: center;align-items: center;background: rgba(0,0,0,.702);z-index: 1025 !important;backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);word-break: keep-all;"></div>
    </div>

    <script>
        $('.share-experience-modal').click(function(e){
            e.preventDefault();
            var link = $(this).attr('href');
            toggleExperiencePopup(link);
        });
        function toggleExperiencePopup(link) {
            var popup = document.getElementById("popup");
            var overlay = document.getElementById("overlay");

            if (window.innerWidth < 992) {
                window.location.href = link;
            } else {
                popup.style.display = (popup.style.display === "block") ? "none" : "block";
                overlay.style.display = (overlay.style.display === "block") ? "none" : "block";
            }
        }
        $('.share-experience-modal-close').click(function(e){
            var popup = document.getElementById("popup");
            popup.style.display = 'none';
            var overlay = document.getElementById("overlay");
            overlay.style.display = 'none';
        });
</script>
</div><script type="text/javascript">
    $(window).on('load', function() {
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "ayc7ypwwuk");
    });
</script>
<!-- Chat bot is being shown for these category articles (8 -> linked-list 9172 -> AI-ML-DS, 1789 -> python  4667 -> math)  -->

</body>
</html>


<!-- Dynamic page generated in 0.983 seconds. -->
<!-- Cached page generated by WP-Super-Cache on 2024-12-18 16:57:09 -->

<!-- Compression = gzip -->
<!-- super cache -->
"""
base_url = "https://www.geeksforgeeks.org/output-java-program-set-7/?ref=rp"
