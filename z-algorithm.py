import sys

PROGRAM_NAME = "exact_pattern_matching.py"
file_name = ""

def output(indices, match, mismatch, comp):
    out_file_name = "output/sol_" + file_name[-1]
    print(f"writing to file {out_file_name}...")
    with open(out_file_name, 'w') as f:
        for i in indices:
            f.write(str(i) + "\n")
        f.write(f"Number of comparisons: {comp}\n")        
        f.write(f"Number of matches: {match}\n")        
        f.write(f"Number of mismatches: {mismatch}\n")        


def match(string, pattern):
    '''
    Using Z-Algorithm
    let's preprocess this pattern first..
    start at index 1, index 0 is uninteresting
    check how much of the suffix we match starting @ curr index
    Z - Algorithm:
    ex T = ACTACTBACTBBDDACBABACTACT
           0003000300000020010600300 <-- z array ; z[3] = 3
    we can find occurences of Pattern P in String S by computing z for P$S.
    occurence starts at i if |z[i]| = |P|
    let try to do process z values for s, linearly

    let k be the index of the character we are currently comparing
    let's define a 'z-box', beginning with left (k) and right (the last matching comparison)
    by definition, the a z-box of length n matches the first chars (the prefix) of the whole string
    so we can use the z-values computed there.

    we can do this UNLESS the z-value PLUS the current index >= right. 
    This is because the next char can be a part of the pattern here, but not previously.
    In which case we have to do our comparisons as usual.

    CASE 1: k > right
        set right, left = k
        - compare string[right] and string[right-left] <-- this is the matching prefix
                                                           aka, right without the offset of left
        - increment right and check again
        - on mismatch, calculate the z val as right-left. This marks the length of our z-box.
    CASE 2: k < right
        CASE 2.1:
            k + z[k-left] < right:
                - it follows that the prefix of this suffix is exactly the same as the prefix of the whole string.
                - set z[k] = z[k-left]
        CASE 2.2:
            k + z[k-left] > right
                - at this point we want to start new comparisons, new z-box:
                - set right, left = k
                - do case 1 essentially
    '''
    num_match = 0
    num_mismatch = 0
    new_string = pattern + "$" + string

    # set up z-array
    z = [0] * len(new_string)
    # step one:
    # go through all chars in string 
    k = 1 # k = 0 is trivial and not worth exploring
    left = 0
    right = 0

    while k < len(new_string):
        if(k > right):
            right = k
            left = k
            while(right < len(new_string) and new_string[right] == new_string[right-left]):
                right += 1
                num_match += 1
            z[k] = right - left
            if right < len(string):
                num_mismatch += 1
        else:
            if(k + z[k-left] < right):
                z[k] = z[k-left]
            else:
                left = k
                while(right < len(new_string) and new_string[right] == new_string[right-left]):
                    right += 1
                    num_match += 1
                z[k] = right - left
                if right < len(string):
                    num_mismatch += 1
        k += 1
    
    # find relevant matches in the actual string, aka everything after |P|+1
    indices = []
    for i in range(len(pattern)+1, len(new_string)):
        if(z[i] == len(pattern)):
            indices.append(i - len(pattern))
    
    num_comp = num_match + num_mismatch    
    output(indices, num_match, num_mismatch, num_comp)

# usage: python3 exact_pattern_matching.py examples_updated/examples/ex_0
if(len(sys.argv) < 2):
    print(f"{PROGRAM_NAME}: missing arg [filename]")
    print(f"{PROGRAM_NAME}: usage: python3 {PROGRAM_NAME} path/to/input/file")
    exit()

file_name = sys.argv[1]
string = ""
pattern = ""
print(f"reading file {file_name}...")
    
with open(file_name, 'r') as f:
    string = f.readline().strip()
    pattern = f.readline().strip()
    match(string, pattern)
