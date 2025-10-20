let pattern_text
let editable_text
let mirror_text
let stats

document.addEventListener("DOMContentLoaded", function() {
    pattern_text = document.getElementById("pattern")
    editable_text = document.getElementById("editable-text")
    mirror_text = document.getElementById("mirror-text")
    stats = document.getElementById("stats")

    pattern_text.addEventListener(('input'), z_algorithm)
    editable_text.addEventListener(('input'), z_algorithm)

    z_algorithm()
})

// port of my python script
function z_algorithm(){
    let string = editable_text.textContent.trim()
    let pattern = pattern_text.textContent.trim()

    let num_match = 0
    let num_mismatch = 0
    let new_string = pattern + "$" + string

    console.log(new_string)

    let z = Array(new_string.length).fill(0)
    let k = 1
    let left = 0
    let right = 0

    while(k < new_string.length){
        if(k > right){
            right = k
            left = k
            while(right < new_string.length && new_string[right] == new_string[right-left]){
                right += 1
                num_match += 1
            }
            z[k] = right - left
            if(right < string.length){
                num_mismatch += 1
            }
        }
        else{
            if(k + z[k-left] < right){
                z[k] = z[k-left]
            }
            else{
                left = k
                while(right < new_string.length && new_string[right] == new_string[right-left]){
                    right += 1
                    num_match += 1
                }
                z[k] = right - left
                if(right < string.length){
                    num_mismatch += 1
                }
            }
        }
        k += 1
    }
    
    stats_inner = `number of comparisons: ${num_match+num_mismatch}; length of string: ${string.length}`
    stats.innerHTML = stats_inner

    // find relevant matches in the actual string, aka everything after |P|+1
    indices = []
    for(let i = pattern.length+1; i < new_string.length; i++){
        if(z[i] == pattern.length){
            indices.push(i - pattern.length - 1)
        }
    }
    console.log(indices)
    populate_mirror(indices, string, pattern)
}

function populate_mirror(indices, string, pattern) {
    let html = `<span style="color: lightpink">${pattern}$</span><br>`;
    let pattern_len = pattern.length
    let current = 0;

    indices.forEach(i => {
        if (i < current) return
        html += string.slice(current, i)
        html += `<span class="highlighted">${string.slice(i, i + pattern_len)}</span>`;
        current = i + pattern_len;
    })

    html += string.slice(current)
    mirror_text.innerHTML = html
}