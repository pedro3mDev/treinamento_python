(function() {
  'use strict';
  const fileBrowseButton = document.querySelector('.file-upload-browse');
  const fileInput = document.querySelector('#id_arquivo');
  const fileInfoInput = document.querySelector('#id_caminho');
  const alert = document.querySelector('.alert');
  const lab = fileInput.parentElement;
  fileBrowseButton.addEventListener('click', function() {
    fileInput.click();});

  fileInput.addEventListener('change', function() {
    const file = this.files[0];

  if (!file.type.match('image/.*')) {
    alert.classList.remove("hidden");
    lab.classList.remove("mb-5");
    this.value = '';
    fileInfoInput.value = '';
    return;
  }else 
  fileInfoInput.value = this.value.replace(/C:\\fakepath\\/i, '');
  alert.classList.add("hidden");
  lab.classList.add("mb-5");
  });
})();


(function($) {
  'use strict';
  $(function() {
    $('.file-upload-browse').on('click', function() {
      var file = $(this).parent().parent().parent().find('.file-upload-default');
      file.trigger('click');
    });
    $('.file-upload-default').on('change', function() {
      $(this).parent().find('.form-control').val($(this).val().replace(/C:\\fakepath\\/i, ''));
    });
  });
})(jQuery);