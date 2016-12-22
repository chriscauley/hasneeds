<post-list>
  <div class="row">
    <div class="col m6 s12" each={ posts }>
      <div class={ theme.outer }>
        <div class={ theme.content }>
          <div class="flexy space-between">
            <a href="/u/{ username }/"><i class="fa fa-slack"> { username }</i></a>
            <div>
              <a href="?has_needs={ has_needs }" class="chip { (has_needs=='has')?'green':'orange' }">
                { has_needs }</a>
              <a href="/c/{ s }/" each={ s in category_pks } class="chip blue lighten-2">{ s }</a>
            </div>
          </div>
          <div class={ theme.header }><a href="/p/{ id }/{ uR.slugify(name) }/">{ name }</a></div>
          <a href="/t/{ s }/" each={ s in tag_pks } class="chip">{ s }</a>
        </div>
      </div>
    </div>
  </div>
  <div id="page-controls">
    <div class="container right-align">
      <a href="/post/new/" class="btn btn-floating btn-large red fa fa-plus"></a>
    </div>
  </div>

  this.on("mount",function() {
    var url = "/durf/board/post/?";
    var matches = this.opts.matches;
    if (matches && matches[1] == 'c') {
      url += "categories__slug="+matches[2];
      this.title = "Category: "+ matches[2];
    }
    if (matches && matches[1] == 't') {
      url += "tags__slug="+matches[2];
      this.title = "Tag: "+ matches[2];
    }
    var has_needs = uR.getQueryParameter("has_needs" || this.opts.location.search || "?");
    if (has_needs) { url+= "&has_needs=" + has_needs; }
    uR.ajax({
      url: url,
      success: function(data) { this.posts = data; },
      that: this,
      target: document.getElementById("content"),
    })
  })
</post-list>

<post-detail>
  <div class={ theme.outer }>
    <div class={ theme.content }>
      <div class="flexy space-between">
        <a href="/u/{ username }/"><i class="fa fa-slack"> { post.username }</i></a>
        <div>
          <a href="/?has_needs={ post.has_needs }" class="chip { (post.has_needs=='has')?'green':'orange' }">
            { post.has_needs }</a>
          <a href="/c/{ s }/" each={ s in post.category_pks } class="chip blue lighten-2">{ s }</a>
        </div>
      </div>
      <div class={ theme.header }>
        <a href="/p/{ post.id }/{ uR.slugify(post.name) }/edit/" if={ can_edit } class="fa fa-edit"></a>
        { post.name }
      </div>
      <a href="/t/{ s }/" each={ s in post.tag_pks } class="chip">{ s }</a>
      <div if={ post.data.external_url }>
        <a href={ post.data.external_url } target="_blank">
          <i class="fa fa-external"></i> { post.data.external_url }
        </a>
      </div>
      <div class="description"></div>
    </div>
  </div>

  uR.ajax({
    url: "/durf/board/post/"+this.opts.matches[1]+"/",
    success: function(data) {
      this.post = data;
      this.root.querySelector(".description").innerHTML = this.post.data.rendered;
      this.can_edit = uR.auth.user.username == data.username || uR.auth.user.is_superuser;
    },
    target: this.root.firstElementChild,
    that: this
  });
</post-detail>

<new-post>
  <div class={ theme.outer }>
    <div class={ theme.header }><h4>New Post</h4></div>
    <div class={ theme.content }>
      <ur-form schema={ opts.schema || uR.schema.new_post } action="/api/board/post/new/" method="POST"></ur-form>
    </div>
  </div>


  var self = this;
  this.on("mount",function() {
    uR.auth.ready(function() {
      if (uR.auth.user.is_superuser && !self.opts.schema) {
        self.opts.schema = uR.schema.new_post.slice()
        self.opts.schema.push({name:"username",required:false});
        self.mount();
      }
    });
  })
</new-post>

<edit-post>
  <div class={ theme.outer }>
    <div class={ theme.header }><h4>
        Edit Post
        <i class="right fa fa-trash" onclick={ delete }></i>
    </h4></div>
    <div class={ theme.content }>
      <ur-form schema={ opts.schema || uR.schema.new_post } initial={ opts.post }
               action="/api/board/post/edit/{ opts.post.id }/" method="POST"></ur-form>
    </div>
  </div>

  var self = this;
  this.on("mount",function() {
    uR.auth.ready(function() {
      if (uR.auth.user.is_superuser && !uR.added_superuser) {
        opts.post.category_pks = opts.post.category_pks[0];
        uR.added_superuser = true;
        self.opts.schema = uR.schema.new_post.slice()
        self.opts.schema.push({name:"username",required:false});
        self.mount();
      }
    });
  })
  delete(e) {
    uR.confirm("Are you sure you want to delete this?",function() {
      uR.ajax({
        url: `/api/board/post/delete/${opts.post.id}`,
        method: "DELETE",
        success: function(data) {
          uR.alert("This post has been deleted");
          uR.route("/");
        }
      });
    });
  }
</edit-post>

<auth-modal>
  <div class={ theme.outer }>
    <div class={ theme.header }><h4>Login Required</h4></div>
    <div class={ theme.content }>
      <p>This app uses the Indy Hall Slack as a login. Please use the link below to connect your slack account to this app.</p>
      <a class="btn btn-large btn-blue" href="/login/slack/?next={ window.location.pathname }">
        <i class="fa fa-slack"></i> Connect with Slack</a>
    </div>
  </div>

  <style>
    auth-modal .card { max-width: 400px; text-align: center; }
    auth-modal p { margin-bottom: 20px !important; text-align: justify; }
  </style>

  this.on("update",function() {
    if (uR.auth.user) { uR.route(window.location.pathname); this.unmount();riot.mount("auth-dropdown") }
  });
</auth-modal>
