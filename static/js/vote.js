$('.js-vote').click(function(ev) {
    var $this = $(this),
        action = $this.data('action'),
        qid = $this.data('qid'); 
    console.log("HERE: "  + action +  " " + qid)
});