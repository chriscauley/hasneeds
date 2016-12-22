uR.auth.login_url = "/login/slack/";
uR.auth.login_icon = "fa fa-slack";
uR.auth.login_text = "Connect with Slack";

uR.addRoutes({
  "^/$": uR.auth.loginRequired("post-list"),
  "^/post/new/$": uR.auth.loginRequired("new-post"),
  "^/(c|t)/([\\w\\d\\-]+)/$": uR.auth.loginRequired("post-list"),
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

uR.schema.fields.description = { type: 'textarea', required: false };
uR.schema.fields.tag_pks = {
  label: "Tags",
  type: 'token-input',
  library: "/api/board/tags/",
}
uR.schema.fields.category_pks = {
  type: 'select',
  choices_url: "/durf/board/category/",
  value_key: 'pk',
  verbose_key: 'pk',
  placeholder: 'Select Category',
}

uR.schema.fields.has_needs = {
  'type': 'select',
  'choice_tuples': [['has', 'I has...'],['needs', 'I needs...']],
}

uR.startRouter();
uR.schema.new_post = [
  { name: 'external_url', required: false,
    help_text: "Optional, this will hepl to populate the rest of the fields" },
  'name',
  'tag_pks',
  'has_needs',
  'category_pks',
  'description',
];
