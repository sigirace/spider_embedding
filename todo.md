[app]
    C
    	- [interface]
    		- DTO(app_id, description, keywords) -> AppSchema(id, app_id, description, keywords, creator, created_at, updated_at)
    	- [service]
    		- create_app (app_shcema)
    	- [repo]
    		- create_app (app_schema)
    R
    	- get_app (id)
    	- [s] get_app_list (user_id)
    U
    	- update_app (app_schema)
    D
    	- delete_app (app_id) [ToDo]
    		- get_app (app_id) -> find_meta_by_app (app_id) -> delete_meta (app_id, meta_id)

[document]

    C
    	- create_document (app_id, files)
    		- document_schema 생성 당시 id 부여
    		- app_id, files
    		- service에서 List를 돌며 Insert
   R
   		- get_document (document_id) : 특정 문서 조회
   		- get_document_by_app (app_id) : 앱에 해당하는 모든 문서 조회
   U
   		- update_document (document_id, param): 특정 문서 수정 -> 필요할까?
   D
   		- delete_document (document_id)
   		- delete_document_list (document_id_list):  
   		

[document]
id
app_id
hash
size
file_path
type:
extension:
file_creation_date:
file_mod_date:

Lifecycle

[chunk]
id
doc_id

page

images
tags
content

Lifecycle


[문서 생성]
- param: app_id

--- 

[문서 청크 생성]
post: /{doc_id}
- body: chunk_size, overlap
	- 해당 문서에 대한 청크를 생성함
	- 만약 이미 청크들이 생성되어있다면, 삭제 후 재생성

create_chunk_by_document
	delete_chunk_by_document_id
		get_chunk_by_document_id
			for chunk delete_chunk
				Rollback -> create_chunk


[청크 집합 생성]
post: /{app_id}
- body: doc_id_list, chunk_size, overlap
- app 단위로 청크 생성

create_chunk_by_app
	get_document_by_app
		for document create_chunk_by_document


[청크 조회]
get: /{chunk_id}
- 해당 chunk id에 대한 청크 조회

get_chunk

[청크 집합 조회]
get: /{doc_id}
- 해당 문서에 대한 전체 청크 리스트 조회

get_chunk_by_document_id

[청크 삭제]
delete: /{chunk_id}
- 해당 청크에 대한 삭제

delete_chunk

[청크 List 전체 삭세]
delete: /{doc_id}/all
- 해당 문서의 전체 청크 리스트 삭제

delete_chunk_by_document_id
	get_chunk_by_document_id
		for chunk_id delete_chunk
			rollback create_chunk


[청크 수정]
put: /{chunk_id}
- body: content, image, tag
	- 해당 청크에 대한 문서 수정
	
[청크 List 삭제]
delete: /{doc_id}/list
- body: chunk_id_list
	- 해당 문서의 청크 리스트에 대한 삭제


[embed-vector]
- id
- doc_id


