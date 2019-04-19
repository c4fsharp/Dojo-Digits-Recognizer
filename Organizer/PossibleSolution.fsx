#load @"..\Dojo\Helper.fsx"
open System.IO

type Image = int []
type Observation = { Label:int; Pixels:Image }
type Model = Image -> int

let euclDistance (img1:Image) (img2:Image) =
    (img1,img2) ||> Seq.map2 (fun x y -> (x-y) * (x-y)) |> Seq.sum

let train trainingSet = 
    let classifier (img:Image) =
        trainingSet
        |> Seq.minBy (fun x -> euclDistance x.Pixels img)
        |> fun obs -> obs.Label
    classifier

let dropHeader (x:_[]) = x.[1..]

let read path =
    File.ReadAllLines(path)
    |> dropHeader
    |> Array.map (fun line -> line.Split(','))
    |> Array.map (fun line -> line |> Array.map int)
    |> Array.map (fun line -> { Label = line.[0]; Pixels = line.[1..] })

let trainingPath = @"c:\users\mathias\documents\visual studio 2012\Projects\Digits-Improve\Digits-Improve\trainingsample.csv"
let training = read trainingPath

let basicModel = train training

let validationPath = @"c:\users\mathias\documents\visual studio 2012\Projects\Digits-Improve\Digits-Improve\validationsample.csv"
let validation = read validationPath

let evaluate (model:Model) =
    validation
    |> Array.averageBy (fun x -> 
        if (model (x.Pixels) = x.Label) then 1. else 0.)

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