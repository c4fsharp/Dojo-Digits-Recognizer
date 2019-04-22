#load @"..\Dojo\Helper.fsx"
open System.IO

type Image = int []
type Observation = { Label:int; Pixels:Image }
type Model = Image -> int

let euclDistance (img1:Image) (img2:Image) =
    (img1, img2)
    ||> Seq.map2 (fun x y -> (x-y) * (x-y))
    |> Seq.sum

let train trainingSet (img:Image) =
    let obs =
        trainingSet
        |> Array.minBy (fun observation ->
            euclDistance observation.Pixels img)
    obs.Label

let dropHeader (x:_[]) = x.[1..]

let read path =
    File.ReadAllLines(path)
    |> dropHeader
    |> Array.map (fun line ->
        let numbers = line.Split ',' |> Array.map int
        { Label = numbers.[0]
          Pixels = numbers.[1..] })

let trainingPath = @"Dojo\trainingsample.csv"
let trainingData = read trainingPath
let basicModel = train trainingData
let validationPath = @"Dojo\validationsample.csv"
let validationData = read validationPath

let evaluate (model:Model) =
    validationData
    |> Array.Parallel.map (fun observation -> 
        if (model (observation.Pixels) = observation.Label) then 1.
        else 0.)
    |> Array.average

evaluate basicModel

// If you want to go further...
// * Try out 1, 2, .. n neighbors?
// * Try out different distances: 
// Manhattan distance: abs(x1-y1 + x2-y2 + ...), 
// "Generalized" distances: abs ((x1-y1)^k + (x2-y2)^k + ...)
// * Try out "blurring" images
// * Try out rescaling pixels to less values, eg. map 0.. 255 to 0..7, 0..15
// Go nuts!

// Blurring: instead of a single pixel,
// we take n x n pixels and average then out.

let size = 28
// compute array index of pixel at (row,col)
let offset row col = (row * size) + col
// compute average over square tile;
// note the array comprehension syntax.
let blur (img:Image) row col rad =
    [| for x in 0 .. (rad-1) do
        for y in 0 .. (rad-1) do
            yield img.[offset (row+x) (col+y)] |]
    |> Array.sum

let blurred n img =
    [| for row in 0 .. (size - n) do
        for col in 0 .. (size - n) do 
            yield blur img row col n |]


// Experiment: try out (hopefully) "better" models!