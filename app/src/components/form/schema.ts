import { array, coerce, number, object, string } from "zod";

const PlayerSchema = object({
  stack: coerce.number().positive().safe(),
  name: string().min(1).max(63).optional(),
});

export const FormSchema = object({
  method: string(),
  payouts: coerce.number().positive().safe().array().min(1),
  players: PlayerSchema.array().min(2),
}).refine((inputs) => inputs.payouts.length <= inputs.players.length, {
  message: "Cannot have more payouts than active players.",
});

export const DefaultValues = {
  method: "malmuth",
  payouts: [100, 50],
  players: [{ stack: 1000 }, { stack: 800 }, { stack: 50 }],
};
