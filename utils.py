from typing import Tuple

import numpy as np
import pandas as pd
import tqdm

FOLDS = [
    ({3, 4, 5, 6, 7, 8, 9}, {2}, {0, 1}),
    ({5, 6, 7, 8, 9, 0, 1}, {4}, {2, 3}),
    ({7, 8, 9, 0, 1, 2, 3}, {6}, {4, 5}),
    ({9, 0, 1, 2, 3, 4, 5}, {8}, {6, 7}),
    ({1, 2, 3, 4, 5, 6, 7}, {0}, {8, 9}),
]

sapsii_columns = ['sapsii']
SAPS_COLUMNS = 'age_score,hr_score,sysbp_score,temp_score,gcs_score,PaO2FiO2_score,bun_score,uo_score,sodium_score,' \
               'potassium_score,bicarbonate_score,bilirubin_score,wbc_score,comorbidity_score,' \
               'admissiontype_score'.split(',')
LABLES_COLUMNS = 'Atelectasis,Cardiomegaly,Consolidation,Edema,Enlarged Cardiomediastinum,Fracture,' \
                 'Lung Lesion,Lung Opacity,No Finding,Pleural Effusion,Pleural Other,Pneumonia,' \
                 'Pneumothorax,Support Devices'.split(',')
TEXT_FEATURES_COLUMNS = [f'text_feature_{i}' for i in range(768)]
<<<<<<< Updated upstream

=======
IMAGE_FEATURES_COLUMNS = [f'image_feature_{i}' for i in range(1024)]
TEXT_TOKEN_FEATURES_COLUMNS = [f'text_token_features_{i}' for i in range(512 * 768)]


device = torch.device('cuda:{}'.format(args.gpus[0]) if torch.cuda.is_available() else 'cpu')

ADJACENCY_MATRIX = torch.tensor([
        [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0], # atelectasis
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], # cardiomegaly
        [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0], # consolidation
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0], # edema
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1], # enlarged cardiomediastinum
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], # fracture
        [1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0], # lung lesion
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0], # lung opacity
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # no finding
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0], # pleural effusion
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0], # pleural others
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0], # pneumonia
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0], # pneumothorax
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0] # support devices
    ], dtype=torch.float, device=device)
>>>>>>> Stashed changes

class Config:
    def __init__(self):
        self.has_saps = False
        self.has_labels = False
        self.has_text_features = False
<<<<<<< Updated upstream
        self.verbose = True
        self.tte_int = False

=======
        self.has_image_features = False
        self.has_text_token_features = False
        self.use_gcn = False
        self.verbose = True
        self.tte_int = False

    def saps(self):
        return self.has_saps \
               and not self.has_labels \
               and not self.has_text_features \
               and not self.has_text_token_features \
               and not self.use_gcn and not self.has_image_features

    def saps_labels(self):
        return self.has_saps \
               and self.has_labels \
               and not self.has_text_features \
               and not self.has_text_token_features \
               and not self.use_gcn and not self.has_image_features

    def saps_text_features(self):
        return self.has_saps \
               and not self.has_labels \
               and self.has_text_features \
               and not self.has_text_token_features \
               and not self.use_gcn and not self.has_image_features

    def saps_text_token_features(self):
        return self.has_saps \
               and not self.has_labels \
               and not self.has_text_features \
               and self.has_text_token_features \
               and not self.use_gcn and not self.has_image_features

    def saps_text_token_features_gcn(self):
        return self.has_saps \
               and not self.has_labels \
               and not self.has_text_features \
               and self.has_text_token_features \
               and self.use_gcn and self.has_image_features
    
    def saps_image_features(self):
        return self.has_saps \
               and not self.has_labels \
               and not self.has_text_features \
               and not self.has_text_token_features \
               and not self.use_gcn and self.has_image_features
    
    def saps_multimodal_features(self):
        return self.has_saps \
               and not self.has_labels \
               and self.has_text_features \
               and not self.has_text_token_features \
               and not self.use_gcn and self.has_image_features
>>>>>>> Stashed changes

class Data:
    def __init__(self, name, config):
        self.name = name
        self.df = None
        self.tte = None
        self.event = None
        self.config = config
        self.x_sksurv = None
        self.y_sksurv = None
        self.x_cctime = None
        self.y_cctime = None
        self.x_pycox = None
        self.y_pycox = None
        self.x_deephit = None
        self.y_deephit = None
        self.text_token_features = None
        self.adj_matrix = None

    def _split_fold(self, fold_indices, name):
        subdata = Data(name, self.config)
        subdata.df = self.df[self.df['fold'].isin(fold_indices)]
        subdata.text_token_features = []
        subdata.adj_matrix = self.adj_matrix

        # print(x)
        if self.text_token_features is not None:
            x = [i for i, fold in enumerate(self.df['fold']) if fold in fold_indices]
            subdata.text_token_features = self.text_token_features[x,:]
        return subdata

    def split3(self, fold) -> Tuple['Data', 'Data', 'Data']:
        return self._split_fold(FOLDS[fold][0], 'train'), \
               self._split_fold(FOLDS[fold][1], 'dev'), \
               self._split_fold(FOLDS[fold][2], 'test')

    def split2(self, fold):
        return self._split_fold(FOLDS[fold][0] | FOLDS[fold][1], 'train'), \
               self._split_fold(FOLDS[fold][2], 'test')

    def _split_instance(self, indices, name):
        subdata = Data(name, self.config)
        subdata.df = self.df.iloc[indices]
        subdata.text_token_features = []
        subdata.adj_matrix = self.adj_matrix
        if self.text_token_features is not None:
            subdata.text_token_features = self.text_token_features[indices, :]
        return subdata

    def describe(self):
        print(self.name)
        print('Len', self.df.shape)


def load_data(top, config) -> Data:
    tte_df = pd.read_csv(top / 'tte.csv', dtype={'study_id': int, 'subject_id': int, 'hadm_id': int})
    if config.tte_int:
        tte_df['time-to-event'] = tte_df['time-to-event'].astype(int)

    df = tte_df
    if config.has_saps:
        sapsii_df = pd.read_csv(top / 'last_visit_sapsii.csv', dtype={'subject_id': int, 'hadm_id': int})
        sapsii_df = sapsii_df.fillna(0)
        hadm_ids = set(tte_df['hadm_id'])
        sapsii_df = sapsii_df[sapsii_df['hadm_id'].isin(hadm_ids)]
        sapsii_df = sapsii_df.set_index(['hadm_id']).reindex(tte_df['hadm_id']).reset_index()
        assert len(sapsii_df) == len(tte_df)
        for i, row in tte_df.iterrows():
            assert row['hadm_id'] == sapsii_df.iloc[i]['hadm_id']
        df = pd.concat([df, sapsii_df[SAPS_COLUMNS]], axis=1)

    if config.has_labels:
        labels_df = pd.read_csv(top / 'mimic-cxr-2.0.0-chexpert.csv', dtype={'study_id': int, 'subject_id': int})
        # labels_df = pd.read_csv(top / 'mimic-cxr-2.0.0-negbio.csv', dtype={'study_id':int, 'subject_id':int})
        labels_df = labels_df.replace(-1, 0.5)
        labels_df = labels_df.replace(0, -1)
        labels_df = labels_df.fillna(0)

        study_ids = set(tte_df['study_id'])
        labels_df = labels_df[labels_df['study_id'].isin(study_ids)]
        labels_df = labels_df.set_index(['study_id']).reindex(tte_df['study_id']).reset_index()
        assert len(labels_df) == len(tte_df)
        for i, row in tte_df.iterrows():
            assert row['study_id'] == labels_df.iloc[i]['study_id']
        df = pd.concat([df, labels_df[LABLES_COLUMNS]], axis=1)

    if config.has_text_features:
<<<<<<< Updated upstream
        # features
        with np.load(str(top / 'chexbert_pooling_features.npz')) as data:
            rows = [data[str(id)][0] for id in tqdm.tqdm(tte_df['study_id'],disable=True)]
        text_features_df = pd.DataFrame(rows, columns=TEXT_FEATURES_COLUMNS)
        assert len(text_features_df) == len(tte_df)
        df = pd.concat([df, text_features_df], axis=1)

    data = Data('whole', config)
    data.df = df
    return data
=======
        with np.load(str(top / 'bluebert_768_features.npz')) as data:
            rows = [data[str(id)][0] for id in tqdm.tqdm(tte_df['study_id'], disable=not config.verbose)]
        text_features_df = pd.DataFrame(rows, columns=TEXT_FEATURES_COLUMNS)
        assert len(text_features_df) == len(tte_df)
        df = pd.concat([df, text_features_df], axis=1)
    
    if config.has_image_features:
        with np.load(str(top / 'densenet121_1024_features.npz')) as data:
            rows = [data[str(id)][0] for id in tqdm.tqdm(tte_df['study_id'], disable=not config.verbose)]
        image_features_df = pd.DataFrame(rows, columns=IMAGE_FEATURES_COLUMNS)
        assert len(image_features_df) == len(tte_df)
        df = pd.concat([df, image_features_df], axis=1)

    data = Data('whole', config)
    data.df = df

    if config.has_text_token_features:
        # features
        with np.load(str(top / 'bluebert_512x768_features.npz')) as npz_file:
            rows = []
            for id in tqdm.tqdm(tte_df['study_id'], disable=not config.verbose):
                features = npz_file[str(id)]
                # features = features.flatten()
                rows.append(features)
        assert len(rows) == len(tte_df)
        data.text_token_features = np.array(rows).reshape(len(tte_df), -1)

    return data
>>>>>>> Stashed changes
