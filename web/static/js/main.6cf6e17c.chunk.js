(this["webpackJsonpkodiak-ui"]=this["webpackJsonpkodiak-ui"]||[]).push([[0],{13:function(e,t,a){},21:function(e,t,a){e.exports=a(33)},26:function(e,t,a){},27:function(e,t,a){},33:function(e,t,a){"use strict";a.r(t);var n=a(0),l=a.n(n),r=a(15),c=a.n(r),o=(a(26),a(13),a(27),a(8)),m=function(e){var t=e.links;return l.a.createElement("nav",{className:"navbar navbar-expand-lg navbar-light bg-light"},l.a.createElement("div",{style:{height:48,display:"flex",alignItems:"center"}},l.a.createElement("img",{alt:"bear",style:{height:128,verticalAlign:"middle"},src:"/bear1.png"})),l.a.createElement(o.b,{className:"navbar-brand",to:"/"},"Kodiak"),l.a.createElement("div",{className:"collapse navbar-collapse",id:"navbarColor03"},l.a.createElement("ul",{className:"navbar-nav mr-auto"},t.map((function(e){return l.a.createElement("li",{className:"nav-item"},l.a.createElement(o.b,{className:"nav-link",to:e.path},e.name))}))),l.a.createElement("form",{className:"form-inline my-2 my-lg-0"},l.a.createElement("input",{className:"form-control mr-sm-2",type:"text",placeholder:"Search"}),l.a.createElement("button",{className:"btn btn-secondary my-2 my-sm-0",type:"submit"},"Search"))))},s=a(5),u=function(e){var t=e.job;return l.a.createElement("tr",null,l.a.createElement("th",{scope:"row"},t.id),l.a.createElement("td",null,t.name),l.a.createElement("td",null,t.repo),l.a.createElement("td",null,l.a.createElement("button",{className:"btn btn-success"},"Run")))},i=function(e){var t=e.jobs;return l.a.createElement("div",{style:{paddingTop:32},className:"container"},l.a.createElement("table",{className:"table table-hover"},l.a.createElement("thead",null,l.a.createElement("tr",null,l.a.createElement("th",{scope:"col"},"ID"),l.a.createElement("th",{scope:"col"},"Name"),l.a.createElement("th",{scope:"col"},"Repo"),l.a.createElement("th",{scope:"col"}))),l.a.createElement("tbody",null,t.map((function(e){return l.a.createElement(u,{job:e})})))))},d=[1,2,3,4,5,6,7,8,9].map((function(e){return{id:e,name:"Job #".concat(e),repo:"https://bitbucket.org/fxqlabs-oss/".concat(e)}})),E=function(){return l.a.createElement(l.a.Fragment,null,l.a.createElement(i,{jobs:d}))},p=a(34),b=a(18),h=function(e){var t=e.run;return l.a.createElement("tr",null,l.a.createElement("th",{scope:"row"},t.id),l.a.createElement("td",null,t.job_id),l.a.createElement("td",null,t.status),l.a.createElement("td",null,"".concat(Object(p.a)(t.started)," ago")),l.a.createElement("td",null,Object(b.a)(t.started,t.ended,{includeSeconds:!0})),l.a.createElement("td",null,l.a.createElement("button",{className:"btn btn-success"},"Action")))},v=function(e){var t=e.runs;return l.a.createElement("div",{style:{paddingTop:32},className:"container"},l.a.createElement("table",{className:"table table-hover"},l.a.createElement("thead",null,l.a.createElement("tr",null,l.a.createElement("th",{scope:"col"},"ID"),l.a.createElement("th",{scope:"col"},"Job ID"),l.a.createElement("th",{scope:"col"},"Status"),l.a.createElement("th",{scope:"col"},"Started"),l.a.createElement("th",{scope:"col"},"Duration"),l.a.createElement("th",{scope:"col"}))),l.a.createElement("tbody",null,t.map((function(e){return l.a.createElement(h,{run:e})})))))},f=a(35),g=a(19),N=[1,2,3,4,5,6,7,8,9].map((function(e){var t=Object(f.a)(Date.now(),100*Math.random()),a=Object(g.a)(t,10*Math.random());return{id:e,job_id:Math.round(10*Math.random()),started:t,ended:a,status:1}})),y=[{name:"Jobs",path:"/jobs",component:E},{name:"Runs",path:"/runs",component:function(){return l.a.createElement(l.a.Fragment,null,l.a.createElement(v,{runs:N}))}}];var k=function(){return l.a.createElement(o.a,null,l.a.createElement("div",{className:"App"},l.a.createElement("header",{className:"App-header"},l.a.createElement(m,{links:y}),l.a.createElement(s.c,null,y.map((function(e){return l.a.createElement(s.a,{path:e.path},e.component)}))))))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));c.a.render(l.a.createElement(l.a.StrictMode,null,l.a.createElement(k,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))}},[[21,1,2]]]);
//# sourceMappingURL=main.6cf6e17c.chunk.js.map