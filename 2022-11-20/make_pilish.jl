# make_pilish.jl
# Christopher Phan
# 2022-11-30
#
# Copyright 2022 Christopher Phan <https://chrisphan.com>
# License: MIT
#
# Produces a Pilish "free verse poem" based on a simple probability model
# from public domain texts.

function add_to_freq_list(d::Dict{String,Int64}, word::String)
    if !(word in keys(d))
        d[word] = 1
    else
        d[word] += 1
    end
end

function add_to_length_list(d::Dict{Int8,Dict{String,Int64}}, word::String)
    ell = length(filter(isletter, word))
    if !(ell in keys(d))
        d[ell] = Dict{String,Int64}()
    end
    add_to_freq_list(d[ell], word)
end

function add_to_pair_list(
    d::Dict{String,Dict{Int8,Dict{String,Int64}}},
    word::String,
    next_word::String,
)
    if !(word in keys(d))
        d[word] = Dict{Int8,Dict{String,Int64}}()
    end
    add_to_length_list(d[word], next_word)
end


function process_file(
    filename::String,
    wp::Dict{String,Dict{Int8,Dict{String,Int64}}},
    tw::Dict{Int8,Dict{String,Int64}},
)
    text = open(f -> readlines(f), filename)
    words = filter(
        x -> (length(filter(isletter, x)) > 0 && length(filter(isletter, x)) < 11),
        [
            lowercase(filter(x -> (isletter(x) || x == '\''), w)) for
            w in reduce(vcat, [split(replace(line, "-" => " "), " ") for line in text])
        ],
    )
    for k in zip(words[begin:end], words[2:end])
        add_to_pair_list(wp, k[1], k[2])
        add_to_length_list(tw, k[1])
    end
end

function get_freq_data(
    filenames::Vector{String},
)::Tuple{Dict{String,Dict{Int8,Dict{String,Int64}}},Dict{Int8,Dict{String,Int64}}}

    word_pairs = Dict{String,Dict{Int8,Dict{String,Int64}}}()
    total_words = Dict{Int8,Dict{String,Int64}}()

    for file in filenames
        process_file(file, word_pairs, total_words)
    end
    return (word_pairs, total_words)
end

function invert_freq_list(d::Dict{String,Int64})::Tuple{Dict{Int64,String},Int64}
    k = Int64(0)
    output = Dict{Int64,String}()
    for key in keys(d)
        output[k] = key
        k += d[key]
    end
    return (output, k)
end

function get_word_from_inv_freq_list(d::Dict{Int64,String}, num::Int64)::String
    sorted_keys = sort([k for k in keys(d)])
    for (idx, key) in enumerate(sorted_keys)
        if key > num
            return d[sorted_keys[idx-1]]
        end
    end
    return d[sorted_keys[end]]
end

function random_word_from_inv_freq_list(d::Dict{Int64,String}, total::Int64)::String
    num = Int64(trunc(rand() * total + 1))
    return get_word_from_inv_freq_list(d, num)
end

function get_next_word(
    wp::Dict{String,Dict{Int8,Dict{String,Int64}}},
    iwp::Dict{String,Dict{Int8,Tuple{Dict{Int64,String},Int64}}},
    itw::Dict{Int8,Tuple{Dict{Int64,String},Int64}},
    word::String,
    next_len::Int8,
)::String
    if next_len in keys(wp[word])
        if !(word in keys(iwp))
            iwp[word] =
                Dict([(len, invert_freq_list(wp[word][len])) for len in keys(wp[word])])
        end
        particular_iwl = iwp[word][next_len]
    else
        particular_iwl = itw[next_len]
    end
    return random_word_from_inv_freq_list(particular_iwl[1], particular_iwl[2])
end

function make_poem(
    digits::Vector{Int8},
    wp::Dict{String,Dict{Int8,Dict{String,Int64}}},
    tw::Dict{Int8,Dict{String,Int64}},
)::Vector{String}
    inv_total_words = Dict([(ell, invert_freq_list(tw[ell])) for ell in keys(tw)])
    inv_word_pairs = Dict{String,Dict{Int8,Tuple{Dict{Int64,String},Int64}}}()

    if digits[1] == 0
        next_len = Int8(10)
    else
        next_len = digits[1]
    end

    output = [
        random_word_from_inv_freq_list(
            inv_total_words[next_len][1],
            inv_total_words[next_len][2],
        ),
    ]
    for k in digits[2:end]
        if k == 0
            next_len = Int8(10)
        else
            next_len = k
        end
        next_word =
            get_next_word(wp, inv_word_pairs, inv_total_words, output[end], next_len)
        output = vcat(output, [next_word])
    end
    return output
end

function word_wrap(words::Vector{String}, len::Int)::Vector{String}
    output = [words[1]]
    for k in words[2:end]
        potential_new_line = output[end] * " " * k
        if length(potential_new_line) <= len
            output[end] = potential_new_line
        else
            output = vcat(output, [k])
        end
    end
    return output
end


# Books from Project Gutenberg

file_list = [
    "pg_books/43-0.txt", # The Strange Case Of Dr. Jekyll
    # And Mr. Hyde, by Robert Louis Stevenson
    "pg_books/pg514.txt", # Little Women, by Louisa May Alcott
    "pg_books/46-0.txt", # A Christmas Carol, by Charles Dickens
    "pg_books/84-0.txt", # Frankenstein, by Mary Wollstonecraft (Godwin) Shelley
    "pg_books/1342-0.txt", # Pride and Prejudice, by Jane Austen
    "pg_books/2701-0.txt", # Moby Dick; or The Whale, by Herman Melville
    "pg_books/pg345.txt", # Dracula, by Bram Stoker
    "pg_books/pg100.txt", # The Complete Works of William Shakespeare
    "pg_books/1400-0.txt", #  Great Expectations, by Charles Dickens
    "pg_books/pg25344.txt", # The Scarlet Letter, by Nathaniel Hawthorne
    "pg_books/pg64317.txt", # The Great Gatsby, by F. Scott Fitzgerald
    "pg_books/160-0.txt", # The Awakening and Selected Short Stories, by Kate Chopin
    "pg_books/4300-0.txt", # Ulysses, by James Joyce
    "pg_books/pg10.txt", # The King James Bible
    "pg_books/3207-0.txt", # Leviathan, by Thomas Hobbes
]

word_pairs, total_words = get_freq_data(file_list)

pi_digits = [parse(Int8, k) for k in "314159265358979323846264338327950288419716939937510"]

pilish = make_poem(pi_digits, word_pairs, total_words)

for line in word_wrap(pilish, 80)
    println(line)
end
