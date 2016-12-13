uR.auth.login_url = "/login/slack/";
uR.auth.login_icon = "fa fa-slack";
uR.auth.login_text = "Connect with Slack";

uR.addRoutes({
  "^/$": function() { uR.mountElement("post-list"); },
  "^/post/new/$": function (path,data) { uR.mountElement("new-post") },
  "^/p/(\\d+)/([\\w\\d\\-]+)/$": function(path,data) { uR.mountElement("post-detail",data); console.log(1);}
});

uR.schema.fields.description = { type: 'textarea' };
uR.schema.fields.tags = {
  type: 'token-input',
  library: "/api/board/tags/",
}
uR.schema.fields.categories = {
  type: 'select',
  choices_url: "/durf/board/category/",
  value_key: 'id',
  verbose_key: 'name',
  placeholder: 'Select Category',
}

uR.startRouter();
uR.schema.new_post = [
  'name',
  'tags',
  'categories',
  'description'
];
uR.auth.ready(function() {
  // there's a race condition here where viewing this page directly causes the form to load before this line :(
  if (uR.auth.user && uR.auth.user.is_superuser) { uR.schema.new_post.push({name:"username",required:False}) }
})
