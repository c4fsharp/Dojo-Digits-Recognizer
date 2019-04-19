[<AutoOpen>]
module Helper

/// Pretty prints the array representation of a number to the console using ASCII art.
let prettyPrint (observation:int []) =
    let printValue =
        let mapping = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ".ToCharArray() |> Array.rev
        let multiplier = float (mapping.Length - 1)
        fun (n:int) -> float n / 256. * multiplier |> int |> Array.get mapping
    observation
    |> Array.map printValue
    |> Array.chunkBySize 28
    |> Array.map System.String
    |> Array.iter (printfn "%s")
