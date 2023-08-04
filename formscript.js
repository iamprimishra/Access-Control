function submitForm() {
    var name = document.getElementById('name').value.trim();
    var accessId = document.getElementById('access-id').value.trim();
    var password = document.getElementById('password').value.trim();
    
    var nameError = document.getElementById('name-error');
    var accessIdError = document.getElementById('access-id-error');
    var passwordError = document.getElementById('password-error');
    
    nameError.innerText = '';
    accessIdError.innerText = '';
    passwordError.innerText = '';
    
    if (name === '') {
      nameError.innerText = 'Please enter your name';
    }
    
    if (accessId === '') {
      accessIdError.innerText = 'Please enter your access ID';
    }
    
    if (password === '') {
      passwordError.innerText = 'Please enter your master password';
    }
    
    if (name !== '' && accessId !== '' && password !== '') {
      var confirmed = confirm('Are you sure you want to submit the form?');
      if (confirmed) {
        document.getElementById('name').value = '';
        document.getElementById('access-id').value = '';
        document.getElementById('password').value = '';
      }
    }
  }
  