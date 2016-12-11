uR.auth.login_url = "/login/slack/";
uR.auth.login_icon = "fa fa-slack";
uR.auth.login_text = "Connect with Slack";

uR.addRoutes({
  "^/$": function() { uR.mountElement("post-list"); },
  "/post/new/": function (path,data) {
    uR.mountElement("new-post")
  },
});

uR.schema.fields.description = { type: 'textarea' };
uR.schema.fields.tags = {
  type: 'token-input',
  library: "/api/board/tags/",
}
