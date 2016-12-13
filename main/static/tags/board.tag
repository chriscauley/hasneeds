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
      <div class={ theme.header }>{ post.name }</div>
      <span each={ n in post.tag_names } class="chip">{ n }</span>
      <div>{ post.data.description }</div>
    </div>
  </div>

  uR.ajax({
    url: "/durf/board/post/"+this.opts.matches[1]+"/",
    success: function(data) { this.post = data; },
    target: this.root.firstElementChild,
    that: this
  });
</post-detail>

<new-post>
  <div class={ theme.outer }>
    <div class={ theme.header }><h4>New Post</h4></div>
    <div class={ theme.content }>
      <ur-form schema={ uR.schema.new_post } action="/api/board/post/new/" method="POST"></ur-form>
    </div>
  </div>

  schema = [
    'name',
    'tags',
    'categories',
    'description'
  ]
  
</new-post>
