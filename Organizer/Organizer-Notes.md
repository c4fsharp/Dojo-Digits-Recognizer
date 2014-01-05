#Script: Comments & Stumbling Blocks

Regularly, people (especially if they came in late and missed the introduction...) don't realize that the first number in each row is the actual digit, i.e. the number itself represented by the following digits, its representation in pixels.

##Section 1. 

People often forget to run the open statements.

##Section 4.

People often get stuck on the idea to have a double map, like this:
data |> Array.map (fun row -> row |> Array.map (fun x -> (int)x))
They also often forget to pipe row into the inside map, resulting in an array of unapplied functions.
A possibly better way to convert to ints is to avoid casting, and simply use int:
data |> Array.map (fun row -> row |> Array.map int)

##Section 5.

People often get stuck on the fact that instantiating a record is as simple as { Label = 1; Pixels = [| 1; 2; 3; |] }

##Section 6.

People sometimes get confused by the example, which shows a distance on 3-elements. The idea is to generalize to arbitrary length arrays.
People often stumble on Array.map2; arguably, Array.map2 is not great, in that it breaks the pattern established before, namely data |> Array.map. The pipe forward operator doesn't work here. Rather than introducing the ||> operator or the concept of tuples, I opted for Array.map2, but this tends to be one of the places where people struggle.

##Section 7 and 8

People often get confused on how to use the training and validation sets, and start doing complicated computations which lead nowhere. The idea here is simple: the only way to evaluate the quality of the classifier is to give it data it has not seen before, and see how much it gets right. So take each example in the validation set, pass it to the classifier and see what it predicts, and compare that to the known, correct value.
Also, people sometimes don't realize that the validation set contains known data as well, i.e. observations where we know from the start what the correct value is.

Typically, when people get a classifier which gets 100% correct, it indicates that they are classifying the training set itself, and not the validation set :)

The expected correct rate is 94.4%

#Possible Conclusion / Opening

Obviously, getting 94.4% correct in 25-ish lines of code is not bad :)
For F# beginners, it's worth pointing out that managing to write a classifier in a language they have not used before is no small feat.

While 94.4% is nice, it's not "done". At that point, 2 directions are possible:
1) the real dataset contains 50,000 elements and not 5,000, which will go 10x slower. One direction is speeding up the algorithm, using maybe Array.parallel.map, or specialized data structures, or other ideas.
2) the model that was built is "the simplest thing that could possibly works", and works pretty well. How can we squeeze more accuracy out of it? There are numerous directions possible, and the only way to know is to just try it, which is why having a validation set (cross-validation) is hugely important: it provides a benchmark for "is the model better or not?". Possible explorations, following the initial model, are: trying 1, 2, 3, ... neighbors (which doesn't work well), trying different distances (which works well but causes technical issues like integer overflow with certain distances), blurring (if you take an image and move it one pixel to the right, the distance might degrade a lot - blurring can compensate for that).
