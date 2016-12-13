uR.auth.login_url = "/login/slack/";
uR.auth.login_icon = "fa fa-slack";
uR.auth.login_text = "Connect with Slack";

uR.addRoutes({
  "^/$": uR.auth.loginRequired("post-list"),
  "^/post/new/$": uR.auth.loginRequired("new-post"),
  "^/p/(\\d+)/([\\w\\d\\-]+)/$": uR.auth.loginRequired("post-detail"),
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
  // since it is currently only a hack for me I'm not going to fix it just yet
  if (uR.auth.user && uR.auth.user.is_superuser) { uR.schema.new_post.push({name:"username",required:false}) }
})
