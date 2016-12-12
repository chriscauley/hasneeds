<post-list>
  <div class="row">
    <div class="col m6 s12" each={ posts }>
      <div class={ theme.outer }>
        <div class={ theme.header }><h4>{ name }</h4></div>
        <div class={ theme.content }>
          <div>{ data.description }</div>
          <span each={ n in category_names } class="chip blue lighten-2">{ n }</span>
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

<new-post>
  <div class={ theme.outer }>
    <div class={ theme.header }><h4>New Post</h4></div>
    <div class={ theme.content }>
      <ur-form schema={ schema } action="/api/board/post/new/" method="POST"></ur-form>
    </div>
  </div>

  schema = [
    'name',
    'tags',
    'categories',
    'description'
  ]
</new-post>
