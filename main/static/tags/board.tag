<post-list>
  <div class="row">
    <div class="{ theme.outer } col m6 s12" each={ posts }>
      <div class={ theme.header }><h4>{ name }</h4></div>
      <div class={ theme.content }>
        { data.description }
      </div>
    </div>
  </div>

  this.on("mount",function() {
    uR.ajax({
      url: "/durf/board/post/",
      success: function(data) { this.posts = data.data; },
      that: this,
      target: document.getElementById("content"),
    })
  })
</post-list>

<new-post>
  <div class={ theme.outer }>
    <div class={ theme.header }><h4>New Post</h4></div>
    <div class={ theme.content }>
      <ur-form schema={ schema }></ur-form>
    </div>
  </div>

  schema = [
    'name',
    'tags',
    'categories',
    'description'
  ]
</new-post>
