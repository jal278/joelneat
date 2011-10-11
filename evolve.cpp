#include "evolve.h"
double bigbuff[LARGESX*LARGESY];
/*
 void artist::optimize(evaluator* e) {
  double oldscore = e->evaluate_artist(this);
  mutate_buffer();
  double newscore = e->evaluate_artist(this);
  if(oldscore>newscore)
   undo_mutate_buffer();
 }

 void artist::optimize(feature_evaluator* e) {
  double oldscore = e->evaluate_artist(this);
  mutate_buffer();
  double newscore = e->evaluate_artist(this);
  if(oldscore>newscore)
   undo_mutate_buffer();
 }
*/
