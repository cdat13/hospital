function addToCart(id, name, description){
    event.preventDefault()

    fetch('/api/medical_report', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'description': description
        }),
        headers: {
        'Content-Type': 'application/json'
        }
    }).then(function(res){
        console.info(res)
        return res.json()
    }).then(function(data){
        console.info(data)
    }).catch(function(err){
        console.err
    })

}

 function updateCart(id, obj) {
    fetch('/api/update-cart',
    {
        method: 'put',
        body: JSON.stringify ({
        'id': id,
        'quantity': parseInt(obj.value)
        }),
        headers: {
        'Content-Type': 'application/json'
         }
     }).then(res => res.json()).then(data =>
     {
//        let quantity = document.getElementById('total-counting')
//        quantity.innerText = data.total_quantity
     })
 }


 function deleteCart(id){
    if(confirm("Bạn chắc chắn muốn xóa loại thuốc này không?") == true )
    {
        fetch('/api/delete-cart/' + id ,
    {
        method: 'delete',
        headers: {
        'Content-Type': 'application/json'
         }
     }).then(res => res.json()).then(data =>
     {
//        let quantity = document.getElementById('total-counting')
//        quantity.innerText = data.total_quantity
//
        let e = document.getElementById("appointment" + id )
        e.style.display = "none"

     }).catch(err => console.error(err))
    }
 }


 function addReport(){
    if(confirm('Ban chac chan muon tao phieu khong?') == true)
    {
        fetch('/api/add-report',
        {
            method: 'post'
        }).then( res => res.json()).then(data => {
            if(data.code == 200)
                location.reload()

        }).catch(err => console.error(err))
    }
 }