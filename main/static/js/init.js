uR.auth.login_url = "/login/slack/";
uR.auth.login_icon = "fa fa-slack";
uR.auth.login_text = "Connect with Slack";

uR.addRoutes({
  "^/$": uR.auth.loginRequired("post-list"),
  "^/post/new/$": uR.auth.loginRequired("new-post"),
  "^/p/(\\d+)/([\\w\\d\\-]+)/$": uR.auth.loginRequired("post-detail"),
  "^/p/(\\d+)/([\\w\\d\\-]+)/edit/$": uR.auth.loginRequired(function(path,opts) {
    uR.ajax({
      url: "/durf/board/post/"+opts.matches[1]+"/",
      success: function(data) {
        opts.post = data;
        opts.post.external_url = data.data.external_url;
        opts.post.description = data.data.description;
        uR.mountElement("edit-post",opts);
      },
    });
  }),
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
  { name: 'external_url', required: false, help_text: "Optional, this will hepl to populate the rest of the fields" },
  'name',
  'tags',
  'categories',
  'description',
];
