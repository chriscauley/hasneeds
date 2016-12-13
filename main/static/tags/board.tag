<post-list>
  <div class="row">
    <div class="col m6 s12" each={ posts }>
      <div class={ theme.outer }>
        <div class={ theme.content }>
          <div class="flexy space-between">
            <a href="/u/{ username }/"><i class="fa fa-slack"> { username }</i></a>
            <a href="/c/{ n }/" each={ n in category_names } class="chip blue lighten-2">{ n }</a>
          </div>
          <div class={ theme.header }><a href="/p/{ id }/{ uR.slugify(name) }/">{ name }</a></div>
          <span each={ n in tag_names } class="chip">{ n }</span>
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
    uR.ajax({
      url: "/durf/board/post/",
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
        <a href="/c/{ n }/" each={ n in post.category_names } class="chip blue lighten-2">{ n }</a>
      </div>
      <div class={ theme.header }>
        <a href="/p/{ post.id }/{ uR.slugify(post.name) }/edit/" if={ can_edit } class="fa fa-edit"></a>
        { post.name }</div>
      <span each={ n in post.tag_names } class="chip">{ n }</span>
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
    <div class={ theme.header }><h4>Edit Post</h4></div>
    <div class={ theme.content }>
      <ur-form schema={ uR.schema.new_post } action="/api/board/post/edit/{ opts.post.id }/" method="POST"
               initial={ opts.post }></ur-form>
    </div>
  </div>

  var self = this;
  this.on("mount",function() {
    uR.auth.ready(function() {
      if (uR.auth.user.is_superuser && !uR.added_superuser) {
        uR.added_superuser = true;
        uR.schema.new_post.push({name:"username",required:false});
        self.mount();
      }
    });
  })
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

</auth-modal>
